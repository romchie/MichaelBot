import sys
from MysteryBox import MysteryBox as mb
db = mb()
db.clearDataBase(sys.argv[1])
print(f'executed clear-db with type {sys.argv[1]}')