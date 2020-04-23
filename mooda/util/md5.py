""" Implementation of md.md5 """
import hashlib


def md5(file_path, save_md5=True, md5_path=None):
    """
    It generates the MD5 code of the input file.
    It saves the code into a file if it save_md5 is True.
    It saves the code into the text file of 'md5_path'.
    If md5_path is None, the name of the file is the same as the input file
    with the md5 extension.

    Parameters
    ----------
        file_path: str
            Path of the file to make the MD5.
        save_md5: bool
            If save_md5 is True, it creates a file with the MD5.
        md5_path: path
            Path of the MD5 file. If md5_path is None, the name of the file is
            the same as the input file with the md5 extension.
    
    Returns
    -------
        haser: str
            MD5 code.
    """

    # Make the MD5 code
    haser = hashlib.md5()
    with open(file_path, 'rb') as open_file:
        content = open_file.read()
        haser.update(content)
    
    if save_md5:
        if md5_path:
            filename_md5 = md5_path
        else:
            # Get the same path but with md5 extension
            parts = file_path.split('.')
            filename_md5 = ""
            for part in parts[:-1]:
                filename_md5 += part
                filename_md5 += '.'
            # write the _<extension>
            filename_md5 = filename_md5[:-1] + '_'
            filename_md5 += parts[-1]

            filename_md5 += ".md5"

        # Save the md5 code into the file
        with open(filename_md5, 'w') as open_file:
            open_file.write(haser.hexdigest())

    return haser.hexdigest()
