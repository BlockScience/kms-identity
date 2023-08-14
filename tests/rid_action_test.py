from rid_lib.core import RID
from rid_lib.means.url import TransformUrl
from rid_lib.means.hackmd import DereferenceHackmd

hackmd = TransformUrl.run(
    RID("url", "https://hackmd.io/uUm16q1oQDmN8T0m9FABNA"),
    {"means": "hackmd"}
)

print(hackmd)

data = DereferenceHackmd.run(hackmd)

print(data)