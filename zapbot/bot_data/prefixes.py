
class Prefixes:

    def __init__(self):

        self.all_prefixes = set()
        self.user_prefixes = set()
        self.admin_prefixes = set()
        self.other_prefixes = dict()

    def add_to_all(self, prefixes):

        prefix_list = self.__guaranteed_prefix_list(prefixes)

        self.all_prefixes.update(prefix_list)
        return self

    def add_to_user(self, prefixes):

        prefix_list = self.__guaranteed_prefix_list(prefixes)

        self.user_prefixes.update(prefix_list)
        return self.add_to_all(prefix_list)

    def add_to_admin(self, prefixes):

        prefix_list = self.__guaranteed_prefix_list(prefixes)

        self.admin_prefixes.update(prefix_list)
        return self.add_to_all(prefix_list)

    def add_to_other(self, type_name: str, prefixes):

        prefix_list = self.__guaranteed_prefix_list(prefixes)

        try:

            self.other_prefixes[type_name].update(prefix_list)

        except KeyError:

            self.other_prefixes[type_name] = set(prefix_list)

        return self.add_to_all(prefix_list)

    @staticmethod
    def __guaranteed_prefix_list(prefixes):

        return prefixes if isinstance(prefixes, list) else [prefixes]


x = Prefixes()

x.add_to_user("b.").add_to_user(['b?', 'b!'])
# x.add_to_user(['b?', 'b!'])
x.add_to_admin(['b::', 'b@'])
x.add_to_other("operator", "b->")
x.add_to_other("operator", "$b ")
x.add_to_other("dj", ["b*"]).add_to_other("dj", 'b|')

# Should do nothing
x.add_to_user("b.")

print("ALL:\t" + x.all_prefixes.__str__())
print("USER:\t" + x.user_prefixes.__str__())
print("ADMIN:\t" + x.admin_prefixes.__str__())
print("OTHER:\t" + x.other_prefixes.__str__())
