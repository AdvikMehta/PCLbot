from db.ASMEKnowledgeStore import ASMEKnowledgeStore

pdf_path = "../test/data/marvel_prop_auction.pdf"
index_name = "asme-bot-knowledge"

query = "How much is the Elektra Natchios’ Overcoat and Pair of Stunt Wakizashis listed for?"

vectordb = ASMEKnowledgeStore(index_name)
print(vectordb.similarity_search(query))

