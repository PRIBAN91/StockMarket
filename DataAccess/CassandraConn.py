from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('deshaw')
