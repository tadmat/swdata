# Indices of movement vector

# Arrow: right hand (dominant hand)
X_POS_R = 0 # 右への移動
X_NEG_R = 1 # 左への移動
Y_POS_R = 2 # 上への移動
Y_NEG_R = 3 # 下への移動
Z_POS_R = 4 # 前方への移動
Z_NEG_R = 5 # 後方への移動
REP_X_R = 6 # 左右移動の繰り返し
REP_Y_R = 7 # 上下移動の送り返し
REP_Z_R = 8 # 前後移動の繰り返し
MULTI_DIR_R = 9 # 複数方向への移動
CIRCLE_R = 10   # 円運動
CURVE_R = 11    # 曲線運動
CROSS_R = 12    # 交差
BEND_R = 13     # 移動方向の途中変化（数値が大きいほど変化が大きい）
CIRCLE_WALL_PALNE_R = 14    # 前方の壁に平行な腕の円運動（手と体の距離は一定．上下左右の円運動）
CIRCLE_HITS_WALL_R = 15     # 前方の壁に向かう腕の円運動（手が前後にも移動する円運動）
CIRCLE_OTHER_R = 16

# Arrow: left hand
X_POS_L = 17 # 右への移動
X_NEG_L = 18 # 左への移動
Y_POS_L = 19 # 上への移動
Y_NEG_L = 20 # 下への移動
Z_POS_L = 21 # 前方への移動
Z_NEG_L = 22 # 後方への移動
REP_X_L = 23 # 左右移動の繰り返し
REP_Y_L = 24 # 上下移動の送り返し
REP_Z_L = 25 # 前後移動の繰り返し
MULTI_DIR_L = 26    # 複数方向への移動
CIRCLE_L = 27   # 円運動
CURVE_L = 28    # 曲線運動
CROSS_L = 29    # 交差
BEND_L = 30     # 移動方向の途中変化（数値が大きいほど変化が大きい）
CIRCLE_WALL_PALNE_L = 31    # 前方の壁に平行な腕の円運動（手と体の距離は一定．上下左右の円運動）
CIRCLE_HITS_WALL_L = 32     # 前方の壁に向かう腕の円運動（手が前後にも移動する円運動）
CIRCLE_OTHER_L = 33

# other movements
CONTACT = 34
FINGER_MOVEMENT = 35
DYNAMICS = 36

ZERO_MOVE = 37      # Movement & Dynamics なし

INDEX_COUNT = 38

# 動作特徴量ごとの重み
FEATURE_WEIGHTS = [
    800, 800, 800, 800, 800, 800, 50, 50, 50, 10, 2000, 50, 500, 500, 500, 500, 500, # 500,
    800, 800, 800, 800, 800, 800, 50, 50, 50, 10, 2000, 50, 500, 500, 500, 500, 500, # 500,
    10,     # Contact
    10,     # Finger movement
    5,      # Dynamics
    500,    # Zero move
]