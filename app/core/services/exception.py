class EntityNotFoundException(BaseException):
    """
    This should be thrown when the entity is not found in the repository
    """

    pass


class UnexpectedEntityException(BaseException):
    """
    This should be thrown when an attempt is made to persist an entity using the
    wrong repository.
    """

    pass
