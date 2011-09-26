from base import BaseProcessor

__all__ = ['DjangoSaver',]

class DjangoSaver(BaseProcessor):
    """
    Convert XML to dict, clean dict, then put that dict into a django model instance and save it.
 
    You'll want to override 'clean', and return the kwargs for the model instance creation.

    We force the use of 'id' for PK.
        
    """
    def __init__(self, model):
        self.model = model
        self.count = 0
        self.fails = 0
        
    def make_params(self, tag):
        raise NotImplemented("Define a `make_kwargs` method that takes an XML tag, and returns a kwargs dictionary which can be passed to a model's `create()` call.")


    @staticmethod
    def _update_or_create(model, get_query, update_kwargs):
        if update_kwargs:
            if get_query:
                get_query['defaults'] = update_kwargs
                m, created = model.objects.get_or_create(**get_query)
                if not created:
                    for k,v in update_kwargs.items():
                        setattr(m, k, v)
                    m.save()
            else:
                m = model.objects.create(**update_kwargs)
            return m
        else:
            return None


    def __call__(self, tag):
        """
        update_or_create(
        """
        get_query, update_kwargs, callback = self.make_params(tag)
        m = DjangoSaver._update_or_create(self.model, get_query, update_kwargs)

        if callback:
            callback(m)

        self.count += 1
        if self.count % 100 == 0:
            print "processed %s items" % self.count