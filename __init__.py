from . import models

def post_init_hook(env):
    """Post-initialization hook to ensure models are properly loaded."""
    # Add any post-initialization logic here if needed 