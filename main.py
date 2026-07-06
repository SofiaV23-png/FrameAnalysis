from models.beam import Beam

beam = Beam(2, 210, 100000000)

beam.add_point_load(1, 1)
beam.add_support(type="pinned", x=0)
beam.add_support(type="roller", x=2)

print(beam.loads)