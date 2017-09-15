//
// Created by zhoushangyue on 17-7-20.
//

#ifndef PROMDNS_SERVICE_MDNS_SOCKET_H
#define PROMDNS_SERVICE_MDNS_SOCKET_H
#define MDNS_PORT 5353//组播端口
#define MDNS_IP "224.0.0.251"//组播地址
#define BUFF_MAX_SIZE 102400
int mDNS_establish();
int mDNS_sendmessage(int fd,char *buffer,int packet_len);
int mDNS_receivemessage(int fd,char *buffer,int packet_len);
#endif //PROMDNS_SERVICE_MDNS_SOCKET_H
