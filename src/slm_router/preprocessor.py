class Preprocessor:

    def process(self, query):
        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        return {
            "original": query,
            "normalized": query.lower(),
            "length": len(query),
            "word_count": len(query.split()),
        }