from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility


def connect_to_milvus(host, port):
    connections.connect("default", host=host, port=port)


def create_collection(collection_name, dim):
    if utility.has_collection(collection_name):
        return Collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="user_data", dtype=DataType.VARCHAR, max_length=65535)
    ]
    schema = CollectionSchema(fields, "TV shows and users collection")
    collection = Collection(collection_name, schema)

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 1024}
    }
    collection.create_index("embedding", index_params)
    return collection


def insert_vectors(collection, vectors, user_data):
    collection.insert([vectors, user_data])


def search_vectors(collection, query_vectors, top_k=5):
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(query_vectors, "embedding", search_params, top_k=top_k, output_fields=["user_data"])
    return results
