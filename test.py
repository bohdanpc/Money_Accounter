if __name__ == "__main__":
    import doctest
    import controller
    import model
    import view
    doctest.testmod()
    doctest.testmod(m=model)
    doctest.testmod(m=controller)
    doctest.testmod(m=view)
