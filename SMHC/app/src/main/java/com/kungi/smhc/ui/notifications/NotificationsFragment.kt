package com.kungi.smhc.ui.notifications

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.firebase.database.*
import com.kungi.smhc.R
import com.kungi.smhc.adapter.NotificationAdapter
import com.kungi.smhc.data.Notification


class NotificationsFragment : Fragment() {

    private lateinit var dbref : DatabaseReference
    private lateinit var notificationRecyclerview : RecyclerView
    private lateinit var notificationList : ArrayList<Notification>
    private lateinit var root: View

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        root = inflater.inflate(R.layout.fragment_notifications, container, false)

        notificationRecyclerview = root.findViewById(R.id.list_notif)
        notificationRecyclerview.layoutManager = LinearLayoutManager(activity)
        notificationRecyclerview.setHasFixedSize(true)

        notificationList = arrayListOf<Notification>()
        getNotifData()

        return root
    }

    private fun getNotifData() {
        dbref = FirebaseDatabase.getInstance().getReference("notifications")

        dbref.addValueEventListener(object : ValueEventListener{

            override fun onDataChange(snapshot: DataSnapshot) {

                if (snapshot.exists()){
                    notificationList.clear()
                    for (dataSnapshot in snapshot.children){
                        Log.d("data snapshot", dataSnapshot.toString())
                        val notification = dataSnapshot.getValue(Notification::class.java)
                        notificationList.add(notification!!)

                    }

                    notificationRecyclerview.adapter = NotificationAdapter(notificationList)

                }

            }

            override fun onCancelled(error: DatabaseError) {
                TODO("Not yet implemented")
            }


        })

    }
}