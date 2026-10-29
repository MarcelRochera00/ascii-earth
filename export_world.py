from ascii_earth import WORLD
import numpy as np

def check_world_bin():
    with open("data/world.bin", "rb") as f:
        raw = f.read()
    
    raw_len = len(raw)
    loaded = np.frombuffer(raw, dtype=np.uint8).reshape(180, 360).astype(bool)
    if raw_len != 64800 or not np.array_equal(WORLD, loaded):
        raise ValueError("world.bin does not match WORLD")


def write_world_in_bin():
    bytes_world = WORLD.astype(np.uint8).tobytes()

    with open("data/world.bin","wb") as f:
        f.write(bytes_world)
    
    check_world_bin()
    
    
def main():
    write_world_in_bin()

if __name__ == "__main__":
    main()