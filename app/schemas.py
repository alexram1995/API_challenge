from app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'fullname', 'photo')

class PublicationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'priority', 'status', 'time_since_published', 'user_id', 'created_at', 'updated_at')

class AccessTokenSchema(ma.Schema):
    class Meta:
        fields = ('access_token', 'user_id')