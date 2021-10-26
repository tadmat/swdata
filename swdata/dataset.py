"""
Dataset for SW transcription data classification
"""
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn.functional as F
import glob
import os
from dataclasses import dataclass
import swdict
from swdict import sign_from_swmlfile, SwDict

@dataclass(frozen=True)
class LabelStruct:
    dirnum: str # number of directory
    gloss: str  # gloss
    labels: list    # label list


@dataclass(frozen=True)
class Transcript:
    sign: swdict.Sign
    labels: list    # target labels (sign ids in swdic.db)

max_nhands = 0
max_nheads = 0
max_nmoves = 0

def sign2tensor(sign: swdict.Sign):
    """convert Sign into tensor
    """
    pad_id = 0      # ID of PAD

    hands = []
    headfacebodies = []
    movements = []

    global max_nhands
    global max_nheads
    global max_nmoves

    for sym in sign.symbols:
        if sym.category == 1:
            hands.append([sym.id, sym.x, sym.y])
        elif sym.category == 4 or sym.category == 5:
            headfacebodies.append([sym.id, sym.x, sym.y])
        else:
            movements.append([sym.id, sym.x, sym.y])

    if len(hands) > max_nheads:
        max_nheads = len(hands)
        print("## nhands updated to", len(hands))
    if len(headfacebodies) > max_nheads:
        max_nheads = len(headfacebodies)
        print("## nheads updated to", len(headfacebodies))
    if len(movements) > max_nmoves:
        max_nmoves = len(movements)
        print("## nmoves updated to", len(movements))

    # max number of hand and head_face_body symbols
    max_hand_symbols = 4
    if len(hands) > max_hand_symbols:
        print("@@@ number of hand symbols:", len(hands))
        print("@@@", hands)
        while len(hands) > max_hand_symbols:
            hands.pop()
    else:
        # fill PAD
        for _ in range(max_hand_symbols - len(hands)):
            hands.append([pad_id, 0, 0])
    max_headfacebody_symbols = 4
    if len(headfacebodies) > max_headfacebody_symbols:
        print("@@@ number of headface_body symbols:", len(headfacebodies))
        print("@@@", headfacebodies)
        while len(headfacebodies) > max_headfacebody_symbols:
            headfacebodies.pop()
    else:
        # fill PAD
        for _ in range(max_headfacebody_symbols - len(headfacebodies)):
            headfacebodies.append([pad_id, 0, 0])


    # max number of movement symbols
    max_movement_symbols = 8
    if len(movements) > max_movement_symbols:
        print("=== number of symbols:", len(movements))
        print("==", movements)
        while len(movements) > max_movement_symbols:
            movements.pop()
    else:
        # fill PAD
        for _ in range(max_movement_symbols - len(movements)):
            movements.append([pad_id, 0, 0])

    #print("****")
    #print([hands, headfacebodies, movements])

    # concatenate hands and headface_body tensor
    hands_heads = hands + headfacebodies

    sym_tensor = torch.LongTensor([
        hands_heads,
        movements,
    ])
    return sym_tensor


class SWDataset(Dataset):
    """Dataset for SW sign classification
    """
 
    def __init__(self, sample_dir=None, use_swdic_data=True, use_swdic_all_entries=False):
        """get data from transcription samples
        """
        if sample_dir is None:
            sample_dir = os.path.join(os.path.dirname(__file__),
                                      "./samples")
        #self.transform = transformer
        self.labels = []
        self.label_vocab = {}
        self.vocab_idx = 0
        sample_list_file = os.path.join(sample_dir, "sample-list.txt")
        if not os.path.exists(sample_list_file):
            print("*** sample-list.txt not found!!")
        else:
            # read labels
            with open(sample_list_file, 'r') as f:
                for line in f:
                    items = line.split()  # ['08', '責任', '2057', '669']
                    dirnum = items[0]   # '08'
                    gloss = items[1]    # '責任'
                    labels = [int(x) for x in items[2:]] # [2057, 669]
                    label_struct = LabelStruct(dirnum, gloss, labels)
                    self.labels.append(label_struct)
                    # insert labels into label_vocab
                    for label in labels:
                        if not label in self.label_vocab:
                            self.label_vocab[label] = self.vocab_idx
                            self.vocab_idx += 1
        
        # Read transcription data
        self.transcripts = []
        sample_dirs = glob.glob(sample_dir + "/[0-9][0-9]_*")
        for dir in sample_dirs:
            num, name = os.path.basename(dir).split('_')
            labels = [x.labels for x in self.labels if x.dirnum == num]
            labels = labels[0]

            files = glob.glob(dir + "/*.swml")
            for file in files:
                sign = sign_from_swmlfile(file)
                data = Transcript(sign=sign, labels=labels)
                self.transcripts.append(data)

        if use_swdic_data:
            # Read signs from swdcit
            swdict = SwDict()
            if not use_swdic_all_entries:
                # use 30 entries
                for signid in self.label_vocab.keys():
                    sign = swdict.search_by_id(signid)
                    data = Transcript(sign=sign, labels=[signid])
                    self.transcripts.append(data)
            else:
                # use all entries
                for signid,sign in swdict.signs.items():
                    data = Transcript(sign=sign, labels=[signid])
                    self.transcripts.append(data)
                    # add signid into label vocabulary
                    if signid not in self.label_vocab:
                        self.label_vocab[signid] = self.vocab_idx
                        self.vocab_idx += 1


    def __len__(self):
        return len(self.transcripts)


    def __getitem__(self, idx):
        # input data
        sign = sign2tensor(self.transcripts[idx].sign)
        #print("*** __getitem___ ***")
        #print(sign)


        # label (tagert): must have exactly one sign ID
        label = self.transcripts[idx].labels[0]
        #print("Label:", label)
        # convert label into index
        label_idx = self.label_vocab[label]
        #label_idx = swdict.signid_vocab[label]

        #print(label_idx)
        return (sign, label_idx)


def main():
    dataset = SWDataset(sample_dir="./samples")
    print('length:', len(dataset))
    sign = dataset[0]

    print(sign)

    dataloader = DataLoader(dataset, batch_size=2, shuffle=False)
    for batch in dataloader:
        print('-----------')
        #print(batch)
        signs, labels = batch
        print("SIGN:", signs)
        print("SIGN SHAPE:", signs.shape)
        print("LABELS:", labels)
        break

if __name__ == "__main__":
    main()
