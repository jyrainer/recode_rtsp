def sanitize_folder_name(stream_url):
    return stream_url.replace(':', '_').replace('/', '_').replace('.', '_')