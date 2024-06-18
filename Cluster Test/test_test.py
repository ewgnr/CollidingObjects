import numpy as np
import pandas as pd
df = pd.DataFrame({
    "NUMBER_OF_COLLISIONS": [10, 20, 10, 30, 60, 70],
    "NUMBER_OF_BALLS": [1, 2, 1, 2, 10,20],
    "NUMBER_OF_LINES": [0, 3, 0, 4, 5,7],
    "NUMBER_OF_TELEPORTS": [0, 0, 1, 2,8, 7],
    "NUMBER_OF_FAILS": [0, 1, 0, 1, 9,4],
    "PLAY_DURATION": [360, 500, 300, 450, 900,200]
})
for i in range(0, 6):
    print (df.iloc[i])

    data = np.concatenate((data1, data2, data3, data4), axis = 0)


import pandas as pd

import numpy as np



df = pd.DataFrame({

  "NUMBER_OF_COLLISIONS": [10, 20, 10, 30, 60, 70],

  "NUMBER_OF_BALLS":   [1, 2,  1,  2,  10, 20],

  "NUMBER_OF_LINES":   [0, 3,  0,  4,  5, 7],

  "NUMBER_OF_TELEPORTS": [0, 0,  1,  2,  8, 7],

  "NUMBER_OF_FAILS":   [0, 1,  0,  1,  9, 4],

  "PLAY_DURATION":    [360,500, 300, 450, 900,200]

})



player_features = 6

player_amount = 6

player = []



for player_index in range(0, player_amount):

  for feature in range(0, player_features):

    player[player_index] = df.loc[feature]