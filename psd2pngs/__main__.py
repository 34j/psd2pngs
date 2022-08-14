from psd2pngs import psd2pngs
import multiprocessing
# this should be called HERE
if __name__ == '__main__': # for pyinstaller to work
    multiprocessing.freeze_support()
    psd2pngs()