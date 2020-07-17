# Lol_Bot2020

Goals :
    (Playing Darius)
    - Beat beginner bot (top lane)
    - Beat intermediate bot (top lane)
    - Buy items
To do:
    <!-- - Buy items level 1. -->
    - If at fountain
        - See if can buy items
        - Move to top
            - Wait for a_minions (Never move forward without minions).
                - Follow a_minions
                - If e_minions
                    -Attack e_minions.
                - If e_champion
                    - Harass e_champion.
                - Commit for kill when enemy champion is low life.
                - If low life
                    - Go under near a_tower
    <---------------- Teleport to fountain .
                



Notes:

States :

    Low life : True
    
    Ally minions near me ? : False
    Ally champions near me ? : True

    Enemy minions near me ? : True
    Enemy champions near me ? : True



main loop:
    while alive
        go to the furthest top tower (look on minimap for the furthest tower)
        if minions near me
            move forward enemy top tower 
            attack enemy minions
            if low life
                teleport to the fountain
                buy items
                restart loop ->
            Harass enemy champion
            Commit for kill when enemy champion is low life.

Lol account list :
    Account 1:
        Email    : maggiesimpsonfirst@gmail.com
        Login    : MaggieFirst
        Password : C**
        Username : MaggieFirst

    Account 2:
        Email    : thanushantharmabalan@hotmail.com
        Login    : RobBott9
        Password : P**
        Username : RobBott9