# To create config servers:
- mongod --dbpath "path\configsvr\cfg1" --logpath "path\configsvr\cfg1\mogod.log" --port 20001 --storageEngine=wiredTiger --journal --replSet cfgsvr --configsvr
- mongod --dbpath "path\configsvr\cfg2" --logpath "path\configsvr\cfg2\mogod.log" --port 20002 --storageEngine=wiredTiger --journal --replSet cfgsvr --configsvr
- mongod --dbpath "path\configsvr\cfg3" --logpath "path\configsvr\cfg3\mogod.log" --port 20003 --storageEngine=wiredTiger --journal --replSet cfgsvr --configsvr

# Inside new terminal
- mongo --port 20001
- rs.initiate(
- {_id:"cfgsvr", configsvr:true,
- members: [
- {_id:0, host:"localhost:20001"},
- {_id:1, host:"localhost:20002"},
- {_id:2, host:"localhost:20003"}
- ]
- }
- )

- rs.status()

# To make shards

## First Shard
- mongod --dbpath "path\shards\shard1\shardsvr1" --logpath "path\shards\shard1\shardsvr1\mongod.log" --port 30001 --storageEngine=wiredTiger --journal --replSet shard1 --shardsvr
- mongod --dbpath "path\shards\shard1\shardsvr2" --logpath "path\shards\shard1\shardsvr2\mongod.log" --port 30002 --storageEngine=wiredTiger --journal --replSet shard1 --shardsvr
- mongod --dbpath "path\shards\shard1\shardsvr3" --logpath "path\shards\shard1\shardsvr3\mongod.log" --port 30003 --storageEngine=wiredTiger --journal --replSet shard1 --shardsvr

# Inside new terminal
- mongo --port 30001
- rs.initiate(
- {_id:"shard1",
- members: [
- {_id:0, host:"localhost:30001"},
- {_id:1, host:"localhost:30002"},
- {_id:2, host:"localhost:30003"}
- ]
- }
- )

- rs.status()

## Second Shard
- mongod --dbpath "path\shards\shard2\shardsvr4" --logpath "path\shards\shard2\shardsvr4\mongod.log" --port 30004 --storageEngine=wiredTiger --journal --replSet shard2 --shardsvr
- mongod --dbpath "path\shards\shard2\shardsvr5" --logpath "path\shards\shard2\shardsvr5\mongod.log" --port 30005 --storageEngine=wiredTiger --journal --replSet shard2 --shardsvr
- mongod --dbpath "path\shards\shard2\shardsvr6" --logpath "path\shards\shard2\shardsvr6\mongod.log" --port 30006 --storageEngine=wiredTiger --journal --replSet shard2 --shardsvr

# Inside new terminal

- mongo --port 30004

- rs.initiate(
- {_id:"shard2",
- members: [
- {_id:0, host:"localhost:30004"},
- {_id:1, host:"localhost:30005"},
- {_id:2, host:"localhost:30006"}
- ]
- }
- )

- rs.status()

# To make router and connect it to config svrs
- mongos --configdb cfg/localhost:20001,localhost:20002,localhost:20003 --port 60000 --logpath "path\router\mongod.log"

# Inside new terminal
- mongo --port 60000
- sh.addShard("shard1/localhost:30001,localhost:30002,localhost:30003")
- sh.addShard("shard2/localhost:30004,localhost:30005,localhost:30006")

- sh.status()

- show dbs
- use eCommerceDB
- sh.enableSharding("eCommerceDB")
- sh.shardCollection("eCommerceDB.api_soldproduct",{"category":"hashed"})
- sh.shardCollection("eCommerceDB.api_myuser",{"username":"hashed"})
- sh.shardCollection("eCommerceDB.api_order",{"id":"hashed"})
- sh.shardCollection("eCommerceDB.api_orderitem",{"id":"hashed"})