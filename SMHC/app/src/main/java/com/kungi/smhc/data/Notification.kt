package com.kungi.smhc.data
import com.google.firebase.database.IgnoreExtraProperties

@IgnoreExtraProperties
class Notification {
    var title : String? = ""
    var content : String? = ""
    var id : String? = ""
    var priority : String? = ""
}