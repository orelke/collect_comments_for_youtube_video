import googleapiclient.discovery as gge

api_key = 'AIzaSyBUt7dFDp63KcOMflf7ksZOYWcbiwxH1og'


def get_all_comments_from_youtube_video(video_id, num_of_comments):
    """
    :param video_id: youtube video id
    :param num_of_comments: to collect.
    :return: dict that contains the video comments in chronological order.
    """
    results = {"comments": []}
    num_of_comments = max(1, num_of_comments)

    try:
        youtube = gge.build('youtube', 'v3', developerKey=api_key)

        video_response = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            order='time',
        ).execute()
        comment_id = 0

        while video_response:
            for item in video_response['items']:
                new_comment = {}

                # Extracting comments:
                top_level_comment = item['snippet']['topLevelComment']['snippet']
                new_comment["textDisplay"] = top_level_comment['textDisplay']
                new_comment["publishedAt"] = top_level_comment['publishedAt']
                total_reply_count = item['snippet']['totalReplyCount']

                # Extracting replies:
                if total_reply_count > 0:
                    new_comment["replies"] = []
                    for reply_id, reply in enumerate(item['replies']['comments']):
                        new_reply = {'textDisplay': reply['snippet']['textDisplay'],
                                     'publishedAt': reply['snippet']['publishedAt']}
                        new_comment["replies"].append(new_reply)

                results["comments"].append(new_comment)
                comment_id += 1
                if comment_id == num_of_comments:
                    return 0, results

            # Pagination handling:
            if 'nextPageToken' in video_response and num_of_comments:
                video_response = youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    order='time',
                    pageToken=video_response['nextPageToken']
                ).execute()
            else:
                break
        return 0, results

    except gge.HttpError as error:
        return 1, {"Status": int(error.status_code), "Type": error.error_details[0]['reason']}
