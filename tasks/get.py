from pathlib import Path
import os
import tarfile
import wget

def metadata(product):
    """
    Get latest metadata table from CORD-19
    """
    logger = logging.getLogger(__name__)
    logger.info("Downloading CORD-19 metadata.csv")
    
    Path(str(product['metadata'])).parent.mkdir(exist_ok=True, parents=True)
    
    wget.download('https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/metadata.csv', out=str(product['metadata']))

def embeddings(product):
    """
    Get latest specter embeddings from CORD-19
    """
    logger = logging.getLogger(__name__)
    logger.info("Downloading CORD-19 embeddings.tar.gz")
    
    Path(str(product)).parent.mkdir(exist_ok=True, parents=True)

    wget.download('https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/cord_19_embeddings.tar.gz', out=str(product))

def extract_embeddings(product, upstream):
    """
    Extract the embeddings archive
    """
    file = tarfile.open(upstream['embeddings'])
    dest = Path(str(product)).parent
    file.extractall(dest)
    file.close()

    for file in os.listdir(dest):
        if file.startswith('cord_19_embeddings'):
            os.rename(os.path.join(dest, file), str(product))