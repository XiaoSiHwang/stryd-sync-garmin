class StrydActivity:
    def __init__(self) -> None:
        self._id = None
        self._activity_id  = None
        self._activity_data = None
        self._is_sync_connect = None
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def setId(self,id):
        self._id = id

    @property
    def activityId(self):
        return self._activity_id
    
    @activityId.setter
    def setActivityId(self,activity_id):
        print(activity_id)
        self._activity_id = activity_id

    @property
    def activityData(self):
        return self._activity_data
    
    @activityData.setter
    def setActivityData(self,activity_data):
        self._activity_data = activity_data
    
    @property
    def isSyncConnect(self):
        return self._is_sync_connect
    
    @isSyncConnect.setter
    def setisSyncConnect(self,is_sync_connect):
        self._is_sync_connect = is_sync_connect