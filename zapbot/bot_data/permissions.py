

# NOTE: original_name preserves the name of the role, with its original casing.
# NOTE: The config data loader should make sure there are copies of names (ignoring casing).
# NOTE: The justification for allowing only uniquely-named permission types is that could simplify
# NOTE: when you have to type the name for a custom type in code, like "@is_type('type name')"
# NOTE: because then the casing could not matter; also, allowing "admin" and "Admin" is kinda dumb.
class PermissionType:

    def __init__(self):

        self.name = None
        # IDEA: Instead of numeric levels for permissions, try set of type names that the type "inherits from".
        # IDEA: Or allow both; implement levels where the code will implicitly calculate inheritance lists,
        # IDEA: and let the user also just state inheritance as another/simpler option if wanted.
        self.level = None
        self.inheritance = set()
        self.prefixes = set()
        self.ids = set()
        self.roles = set()

    def __str__(self):

        set_str = lambda s: s.__str__() if s else "{}"

        result = f"NAME:\t\t{self.name}\n" \
                 f"LEVEL:\t\t{self.level}\n" \
                 f"PREFIXES:\t{set_str(self.prefixes)}\n" \
                 f"IDS:\t\t{set_str(self.ids)}\n" \
                 f"ROLES:\t\t{set_str(self.roles)}\n" \
                 f"INHERITS:\t{set_str(self.inheritance)}\n"

        return result

    def set_name(self, original_name: str):

        self.name = original_name
        return self

    def set_level(self, level):

        self.level = level
        return self

    def add_prefixes(self, prefixes):

        prefix_list = self.__guaranteed_list(prefixes)
        self.prefixes.update(prefix_list)
        return self

    def add_ids(self, ids):

        id_list = self.__guaranteed_list(ids)
        self.ids.update(id_list)
        return self

    def add_roles(self, roles):

        role_list = self.__guaranteed_list(roles)
        self.roles.update(role_list)
        return self

    def add_inherit(self, inherited_roles):

        inheritance_list = self.__guaranteed_list(inherited_roles)
        self.inheritance.update(inheritance_list)
        return self

    @staticmethod
    def __guaranteed_list(given_data):
        return given_data if isinstance(given_data, list) else [given_data]


# NOTE: Justification for including more built-in permission types is that each built-in type
# NOTE: will be able to support custom methods and procedures.
# NOTE: This could nicely enhance the experience when working with common permission types, such
# NOTE: as mod/admin/etc; e.g. "@is_mod()" is nicer than something like "@is_type('mod')".
class PermissionTypes:

    def __init__(self):

        self.all = PermissionType()
        self.everyone = PermissionType()
        self.member = PermissionType()
        self.demimod = PermissionType()
        self.mod = PermissionType()
        self.admin = PermissionType()
        self.others = dict()

    def __str__(self):

        breaker = "---------------------------------------"
        result = f"MEMBER:\n{breaker}\n{self.member}\n\n" \
                 f"DEMIMOD:\n{breaker}\n{self.demimod}\n\n" \
                 f"MOD:\n{breaker}\n{self.mod}\n\n" \
                 f"ADMIN:\n{breaker}\n{self.admin}\n\n"

        for other_type_name, other_type_data in self.others.items():

            result += f"{other_type_name.__str__().upper()}:\n{breaker}\n{other_type_data}\n\n"

        return result

    def add_to_member(self, level: float=None, prefixes=[], ids=[], roles=[], inheritance=[]):

        self.member.set_level(level).add_prefixes(prefixes).add_ids(ids).add_roles(roles).add_inherit(inheritance)
        self.all.add_prefixes(prefixes)
        return self

    def add_to_demimod(self, level: float=None, prefixes=[], ids=[], roles=[], inheritance=[]):
        self.demimod.set_level(level).add_prefixes(prefixes).add_ids(ids).add_roles(roles).add_inherit(inheritance)
        self.all.add_prefixes(prefixes)
        return self

    def add_to_mod(self, level: float=None, prefixes=[], ids=[], roles=[], inheritance=[]):
        self.mod.set_level(level).add_prefixes(prefixes).add_ids(ids).add_roles(roles).add_inherit(inheritance)
        self.all.add_prefixes(prefixes)
        return self

    def add_to_admin(self, level: float=None, prefixes=[], ids=[], roles=[], inheritance=[]):

        self.admin.set_level(level).add_prefixes(prefixes).add_ids(ids).add_roles(roles).add_inherit(inheritance)
        self.all.add_prefixes(prefixes)
        return self

    def add_to_other(self, type_name: str, level: float=None, prefixes=[], ids=[], roles=[], inheritance=[]):

        if type_name in self.others:

            self.others[type_name]\
                .set_level(level).add_prefixes(prefixes).add_ids(ids).add_roles(roles).add_inherit(inheritance)

        else:

            self.others[type_name] = PermissionType()\
                .set_name(type_name).set_level(level).add_prefixes(prefixes)\
                .add_ids(ids).add_roles(roles).add_inherit(inheritance)

        self.all.add_prefixes(prefixes)

        return self

    def determine_inheritance_from_levels(self):

        for permission_type in self.others.values():

            if permission_type.level is None:
                continue

            inherited_types = [types for types in self.others.values()
                               if types.level is not None and types is not permission_type]

            inherited_types = [types.name for types in inherited_types if types.level < permission_type.level]

            permission_type.add_inherit(inherited_types)

    def determine_inheritance_from_explicit(self):

        pass


x = PermissionTypes().add_to_member(prefixes=['b.', 'b?', 'b!']).add_to_admin(prefixes='b@').add_to_admin(prefixes='b::')
x.add_to_other(type_name="DJ", prefixes=["b*", 'b|'], level=2, ids='22142412', roles=['4124441242142', '234235235'])
x.add_to_other(type_name="Cool Guy", prefixes="world").add_to_other(type_name="Cool Guy", prefixes="hello", level=3)
x.add_to_other(type_name="Super ADMIN", prefixes="$b ", level=float('inf'))
# x.add_to_other(type_name="Super ADMIN")
x.determine_inheritance_from_levels()

print(x)
