""" Implementation of md.md5 """
import hashlib


def md5(file_path, save_dm5=True, md5_path=None):
    """
    It generates the MD5 code of the input file.
    It saves the code into a file if it save_md5 is True.
    It saves the code into the text file of 'md5_path'.
    If md5_path is None, the name of the file is the same of the input file
    with the md5 extension.
    """

    # Make the MD5 code
    haser = hashlib.md5()
    with open(file_path, 'rb') as open_file:
        content = open_file.read()
        haser.update(content)
    
    if save_dm5:
        if md5_path:
            filename_md5 = md5_path
        else:
            # Get the same path but with md5 extension
            parts = file_path.split('.')
            filename_md5 = ""
            for part in parts[:-1]:
                filename_md5 += part
            filename_md5 += ".md5"

        # Save the md5 code into the file
        with open(filename_md5, 'w') as open_file:
            open_file.write(haser.hexdigest())

    return haser.hexdigest()