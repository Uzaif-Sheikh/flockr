# ITTERATION 1 ASSUMPTIONS
* When we are working on testing one function in any test, we assume all other functions are working perfectly.

* To check that the token returned/sent is a valid token, we store a list (uid,token) tuple in a special data structure called tokens
in data_storage.py, which helps us in identifying the validity of token.

* For the creation of token in auth.py we take a random integer and then append it with the email id to identify the user uniquely.

* In auth.py we assume that if the user registers for the first time, then the (uid,token) pair returned by login is the same as the register but after user logs out then in our data structure which we have specially created for storing (uid,token) token pair we set the token to NULL to signify the end of current log in session and next time the user logs in we set a new token for the user signifying the beginning of new log in session using the method defined in (3).

* We assume that if a person tries to log in again when that person is already logged in then the auth_login() returns the same (uid,token) pair to signify that the user is in the same log in session and all the functions uses the same token to work the same way as they
did earlier, which means that if a user tries to log in again when he is already logged in no effect happens.

* A member who is already in the group can not be invited again

* For channel_join, we assume the person trying to join the channel must be not already be a member

* Assumed the autherised user leaving the channel in channel_leave could be anyone (either a member or an owner)

* We assume owners must also be added to the member list of a channel.

* We have assumed that if the last memeber in the channel leaves the channel then the channel exists as it is, be it public or private but we dont delete it.

* Assumed channel_addowner and channel_removeowner CAN be performed on the Flockr owner, because they must be an owner of any channel they're in as per the spec (6.6. Permissions)

* Assumed addowner can only be performed on users who are already part of the channel

* Assumed the Flockr owner may be invited to a channel despite being able to just join whatever channel they want

* When Flockr owner joins/is invited to a channel they must immediately be added as an owner // THIS ASSUMPTION WAS CHANGED FOR ITERATION 2

* Assumed it is NOT possible for the Flockr owner to specifically perform an invite to a channel they are not a part of.

* In channel_messages start should not be less than 0.

* Assume that if all users have left the chat then channel exists and we dont delete it.

* We assume that an owner may remove themselves as owners

* Addowner may not be called on a user who is not a member of the channel

* Flockr owner can add anyone as owner of a channel, even if they aren't a part of that channel

* As per forum talks, we assume we cannot check the input error for checking for start value greater than the number of messages in iteration 1 as we need messages_send to implement this.

* We have assumed that the channel_create() function will generate an input error if channel name is left empty.

* Assumed that channels functions generate an TokenError if the given token is invalid.

* We assume that the list function in channels displays a list of all the channels that the user is a member or owner of currently.

* Listall function in channels also displays the list of channels whose visibility has been set to private by the owner.

* If a channel has only one owner/member and he/she decides to leave the channel, the channel will be removed from the list function of the associated member who just left, but will still be displayed in the listall function since it shows the list for all members not for a particular member.

# FURTHER ASSUMPTIONS/CHANGES IN ASSUMPTIONS MADE IN ITERATION 2
The extra assumptions made during this iteration involved:

* We CHANGED an assumption from iteration 1 which now suggests that the flockr owner MAY be added/removed as an owner of the channel and will NOT automatically be added as an owner.

* On the frontend exemplar website given to us there was an issue: the flockr owner is given a star even though they are not added as owners of the channel. Because all previous illustrations told us NOT to automatically add the owner of flockr as the owner of the channel (see forum post https://piazza.com/class/kd1uk6k7tv91ha?cid=365), we decided to keep our implementation as is. This was fueled by much discussion on the forum.

* We assume that the user can see the channels they are a part of even if these channels are private.

* We assume that a person who is added as a flockr owner by the original flockr owner is able to strip the original flockr owner of their owner permissions.

* The tokens passed into all message and user functions represented valid authorised users

* Only a flockr owner may use admin/userpermission/change to change someone's global permissions

* Only first name and last name are offered on registration, no middle name etc.

* We assume that there are only two integers used to represent global permissions: 1 for Owner, 2 for member.


