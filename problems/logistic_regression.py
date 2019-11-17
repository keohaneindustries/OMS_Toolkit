# %% imports
from myimports import *
from lib.data.load.rock_lobster import RockLobsterData

# %%
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]
              ], dtype=float)

print("A[:, :] ==\n", A)
print("\na0 := A[:, 0] ==\n", A[:, 0])
print("\na1 := A[:, 2:3] == \n", A[:, 2:3])

print("\nAdd columns 0 and 2?")
a0 = A[:, 0]
a1 = A[:, 2:3]
print(a0 + a1)

# %% load the data
df_lobsters = RockLobsterData.load_these_lobsters(temp=True, plot=False)

# %%

# %%

# %%
