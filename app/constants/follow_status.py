from enum import Enum

class FollowStatus(str, Enum): # chances of writing may incrasae the typo error chances so defining and using it everywhere  is best practice
    FOLLOWING = "following"
    NOT_FOLLOWING = "not_following"

