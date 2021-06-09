package com.kungi.smhc.holders

import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.kungi.smhc.data.Notification
import kotlinx.android.synthetic.main.item_notification.view.*

class NotificationViewHolder (itemView: View) : RecyclerView.ViewHolder(itemView) {
    fun bindMessage (notif: Notification?) {
        with(notif!!) {
            itemView.tv_prioritas.text = priority
            itemView.tv_title.text = title
        }
    }

}