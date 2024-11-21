from langchain.text_splitter import CharacterTextSplitter
import os


def chunk_doc(document: str, output_dir="data/chunks"):
    """
    Function to chunk a document and save the chunks as text files.

    Parameters:
    - document (str): The text document to chunk.
    - output_dir (str): The directory where chunk files will be saved.

    Returns:
    - List of chunks (str).
    """
    try:
        # Configure the text splitter
        text_splitter = CharacterTextSplitter(
            chunk_size=35, chunk_overlap=0, separator=" ", strip_whitespace=True
        )

        # Chunk the document
        chunks = text_splitter.split_text(document)

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save each chunk to a separate file
        for i, chunk in enumerate(chunks):
            with open(f"{output_dir}/chunk_{i+1}.txt", "w", encoding="utf-8") as file:
                file.write(chunk)

        print(f"Chunks saved successfully in {output_dir}.")
        return chunks

    except Exception as e:
        print(f"Error while chunking the document: {e}")
        return []


# Example usage
if __name__ == "__main__":
    example_document = """
    This is a simple example text to demonstrate how chunking works with the LangChain library.
    Each chunk will have a maximum size of 35 characters. The output will be saved as text files.
    This ensures the chunks are easy to handle in downstream processes.
    """

    chunks = chunk_doc(example_document)
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk}")
