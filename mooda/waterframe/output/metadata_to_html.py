import flask
import os


def metadata_to_html(self, filename=None, logo_link=None, footer_text=''):
    """
    Make a html file with the metadata information.

    Parameters
    ----------
        filename: str
            Filename and path of the html file. If filename is None, the file will be saved in the
            root folder with the name of the metadata['id'].
        logo_link: str
            URL with the logo to be placed on the medatada file.
        footer_text: str
            Text to be placced on the footer of the html file.
    
    Returns
    -------
        filename: str
            Name of the html file.
    """
    # Find the path to the html templates directory
    dirname = os.path.dirname(__file__)
    template_folder = os.path.join(dirname, 'html_templates')

    # Look for the filename, that is equal to self.metadata['id']
    # If self.metadata['id'] does not exist, filename is 'metadata.html'
    if filename is None:
        filename = self.metadata.get('id', 'metadata') + '.html'

    app = flask.Flask('my metadata', template_folder=template_folder)

    with app.app_context():
        rendered = flask.render_template(
            'metadata.html',
            logo_link=logo_link,
            metadata_dict=self.metadata,
            footer_text=footer_text
        )

    with open(filename, 'w') as handle:
        handle.write(rendered)
    
    return filename
