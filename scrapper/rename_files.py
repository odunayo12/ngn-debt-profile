# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import glob
import os
# %%
files_dir = glob.glob(r"C:\Users\rotim\Downloads\*iconfinder*")
len(files_dir)

# %%
#file_ext = [item.rsplit(".", 1)[1] for item in files_dir]
#filename_s =[i for i in range(1, len(file_ext))]
# %%
os.getcwd()


# %%

# %%


# %%
for index, ext_ in enumerate(files_dir):
    ext_1 = ext_.rsplit("\\", 1)
    ext_2 = ext_1[1].rsplit(".", 1)
    os.chdir(ext_1[0])
    web = os.rename(os.path.join(ext_1[0], ext_1[1]), os.path.join(
        ext_1[0], ''.join([str(index+1)+".", ext_2[1]])))
    # print(ext_1[0],ext_2[0],ext_2[1])
