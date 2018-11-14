import peewee as pw
import helpers


# Create the database.
db = pw.SqliteDatabase('accounts.db')


# Named 'Password' because the most important thing
# about the class use is the name of the site the password is for.
class Password(pw.Model):
    # Establish class parameters.
    name = pw.CharField()
    length = pw.IntegerField(default=8)
    symbols = pw.BooleanField(default=True)
    # Will fill it up with the get_accepted_chars function.
    characters = pw.CharField(default='')

    class Meta:
        database = db

    # Check which characters are accepted and add to final list.
    def get_accepted_chars(self):
        # If characters have already been provided, use them instead.
        if self.characters:
            return self.characters
        accepted_chars = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                          'abcdefghijklmnopqrstuvwxyz'
                          '0123456789')
        if self.symbols:
            accepted_chars += '!@#$%^&*()-_'
        # Returns string of all accepted chars for this password.
        return accepted_chars

    # Create the password using the helper functions from the other file.
    def password(self, plaintext):
        return helpers.password(plaintext, self.name, self.length)


# Connect to database, create table if it doesn't already exist.
def initialize_db():
    db.connect()
    db.create_tables([Password], safe=True)
    db.close()


initialize_db()


# Generate a new password.
new_entry = Password.create(name='facebook', length=12, symbols=True)
# Save the entry info in the database, so you can look up your password any time.
new_entry.save()

# Use something easy to remember as salt, since you'll be safe with your MASTER_KEY.
p = new_entry.password('password123')
# Copy-paste to the sing-up form for the site you want and you're done.
print(p)
