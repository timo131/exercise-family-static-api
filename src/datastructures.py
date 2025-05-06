"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list
"""

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = [
            {
                "id": self._generate_id(),
                "first_name": "John",
                "last_name": last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            }
        ]

    # This method generates a unique incremental ID
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        member["id"] = self._generateId()
        member["last_name"] = self.last_name
        self._members.append(member)
        print("self members", self._members)
        return member
    
    def update_member(self, id, new_data):
        updatable_fields = {"first_name", "age", "lucky_numbers"}
        
        for member in self._members:
            if member["id"] == id:
                for key, value in new_data.items():
                    if key in updatable_fields:
                        member[key] = value
            print("Member updated:", self._members)
            return member

    def delete_member(self, id):
        for member in self._members:
            if member["id"] == id:
                self._members.remove(member)
                print("Member deleted:", member)
                return True
        return False

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                print("Member:", member)
                return member

    # This method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members