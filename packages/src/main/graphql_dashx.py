import graphene


class User(graphene.ObjectType):
    id = graphene.ID()
    userName = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    emailId = graphene.String()


class Query(graphene.ObjectType):
    users = graphene.List(User, first=graphene.Int())

    def resolve_users(self, info, first):
        return [
            User(userName="vikrantvkk", firstName="Vikrant", lastName="Vishwakarma",
                 emailId="vikrant.vishwakarma07@gmail.com")
        ][:first]


class CreateUser(graphene.Mutation):

    class Arguments:
        userName = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, userName):
        user = User(userName=userName)
        return CreateUser(user=user)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)

result = schema.execute(
    '''
    mutation createUser{
        createUser(userName: "vikrantvkk") {
            user {
                userName
            }
        }
    }
    '''
)

items = dict(result.data.items())

print(items)
