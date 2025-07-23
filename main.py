import json

class InstagramAnalyzer:
    def __init__(self, following_file_path, followers_file_path):

        self.following_file = following_file_path
        self.followers_file = followers_file_path
        self.following_list = self._extract_usernames(self.following_file)
        self.followers_list = self._extract_usernames(self.followers_file)

    def _extract_usernames(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Standard Instagram JSON export format can vary slightly.
                # This handles the common format where usernames are in a list of relationships.
                if isinstance(data, dict):
                    # Handles format: {"relationships_following": [...]}
                    key = list(data.keys())[0]
                    data = data[key]

                # Each item in the list is a dict containing 'string_list_data'
                usernames = [
                    item['string_list_data'][0]['value']
                    for item in data
                ]
                return usernames
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return []
        except (KeyError, IndexError):
            print(f"Error: Could not parse the file '{file_path}'. Ensure it is the correct Instagram JSON file.")
            return []


    def find_non_followers(self):
        """
        Compares the following and followers lists to find users who don't follow back.

        Returns:
            A sorted list of usernames that you follow but don't follow you back.
        """

        followers_set = set(self.followers_list)

        # Find users in the following list who are not in the followers set.
        non_followers = [
            user for user in self.following_list if user not in followers_set
        ]

        # Return the list sorted alphabetically.
        return sorted(non_followers)


if __name__ == "__main__":
    # Define the names of your JSON files.
    # Ensure these files are in the same directory as the script.
    FOLLOWING_JSON = 'following.json'
    FOLLOWERS_JSON = 'followers.json'

    analyzer = InstagramAnalyzer(FOLLOWING_JSON, FOLLOWERS_JSON)

    # Find the users who don't follow you back
    not_following_back = analyzer.find_non_followers()

    # Print the results
    if not_following_back:
        print("Accounts you follow that don't follow you back:")
        print("--------")
        # Print each username on a new line for clarity
        for username in not_following_back:
            print(username)
    else:
        print("No accounts found that don't follow you back! You're all good.")