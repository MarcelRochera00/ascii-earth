from ascii_earth import WORLD
import numpy as np

def check_world_bin():
    with open("data/world.bin", "rb") as f:
        raw = f.read()
    
    raw_len = len(raw)
    loaded = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))[: 180 * 360].reshape(180, 360).astype(bool)
    if raw_len != 8100 or not np.array_equal(WORLD, loaded):
        raise ValueError("world.bin does not match WORLD")


def write_world_in_bin():
    bytes_world = np.packbits(WORLD.astype(np.uint8)).ravel()
    

    with open("data/world.bin","wb") as f:
        f.write(bytes_world)
    
    check_world_bin()
    
    
def main():
    write_world_in_bin()

if __name__ == "__main__":
    main()