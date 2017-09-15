//
// Created by zhoushangyue on 17-7-10.
//
#include<sys/types.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include "mDNS.h"
#include "mDNS_socket.h"

void dealstring(char *fname,char *name){
    int begin=0;
    int end=0;
    int i=0;

    for(int i=0;i<strlen(name);i++)
    {
        end=i;
        if(begin>end)
        {
            printf("Wrong while dealstring!\n");
            exit(66);
        }
        if(name[i]=='.') {
            sprintf(fname + begin, "%c", end - begin);
            strncpy(fname + begin + 1, name + begin, end - begin);
            begin = end + 1;
        }
    }
    end++;
    sprintf(fname+begin,"%c",end-begin);
    strncpy(fname+begin+1,name+begin,end-begin);
}//将名字等字符串处理为可以在网络中传输的格式；


void ip4_PTR(char *iptr,char* ip)
{
    u_int32_t ipd=inet_addr(ip);
    u_int8_t temp[5];
    memcpy(temp,&ipd,sizeof(ipd));
    sprintf(iptr,"%d.%d.%d.%d.in-addr.arpa",temp[3],temp[2],temp[1],temp[0]);
}//将字符串形式的IPv4转化为ptr地址；

void set_mDNSheader(mDNS_HEADER *header,u_int16_t transaction,u_int16_t flags,
                    u_int16_t questioncnt,u_int16_t answercnt,u_int16_t authoritycnt,
                    u_int16_t additonalcnt)
{
    bzero(header,sizeof(mDNS_HEADER));
    header->TRANSACTION=htons(transaction);
    header->FLAGS=htons(flags);
    header->QUESTION_COUNT=htons(questioncnt);
    header->ANSWER_COUNT=htons(answercnt);
    header->AUTHORITY_COUNT=htons(authoritycnt);
    header->ADDITONAL_COUNT=htons(additonalcnt);
}//mDNS报文头部处理为可以在网络中传输的格式


int set_mDNS_RRecord(RRecord *rr,char *name,char *data,u_int16_t type,u_int16_t class,
                     u_int32_t ttl,u_int16_t length,
                     u_int16_t priority,u_int16_t weight,u_int16_t port)
{
    int len=0;
    rr->name=(char *)calloc(1024,sizeof(char));
    rr->rdata=(char *)calloc(1024,sizeof(char));
#ifdef Debug
    printf("before:%s\n",rr->name);
#endif
    dealstring(rr->name,name);
    printf("after:%s\n",rr->name);
    len+=strlen(rr->name)+1;
    rr->type=htons(type);
    rr->class=htons(class);
    rr->ttl=htonl(ttl);
    rr->length=htons(length);

    len+=10;
    int po=0;
    if(priority!=NOTEXIST && weight!=NOTEXIST && port!=NOTEXIST)
    {
        priority=htons(priority);
        memcpy(rr->rdata+po,&priority,sizeof(priority));
        po+=sizeof(priority);
        weight=htons(weight);
        memcpy(rr->rdata+po,&weight,sizeof(weight));
        po+=sizeof(weight);
        port=htons(port);
        memcpy(rr->rdata+po,&port,sizeof(port));
        po+=sizeof(port);
    }
    if(type==1)
    {
        u_int32_t d=inet_addr(data);
        memcpy(rr->rdata+po,&d,4);
    }

    else {
        dealstring(rr->rdata + po, data);
    }

    len+=length;

    return len;
}//资源记录处理为可以在网络中发送的格式

int set_mDNS_QRecord(QRecord *qr, char *name, u_int16_t type,u_int16_t class)
{
    int len=0;
    qr->name=(char *)calloc(1024,sizeof(char));
    dealstring(qr->name,name);
    printf("%s\n",qr->name);
    len+=strlen(qr->name)+1;
    qr->type=htons(type);
    qr->class=htons(class);
    len+=4;
    return len;
}//查询处理为可以在网络中发送的格式


void write_data(mDNS_PACKET pa,char* buffer)
{
    int po=0;
    memcpy(buffer,&pa.header,sizeof(pa.header));
    po+=sizeof(pa.header);
    for(int i=0;i<ntohs(pa.header.QUESTION_COUNT);i++) {
        memcpy(buffer + po, pa.question[i].name, strlen(pa.question[i].name) + 1);
        po += strlen(pa.question[i].name) + 1;
        memcpy(buffer + po, &pa.question[i].type, sizeof(pa.question[i].type));
        po += sizeof(pa.question[i].type);
        memcpy(buffer + po, &pa.question[i].class, sizeof(pa.question[i].class));
        po += sizeof(pa.question[i].class);
    }
    for(int i=0;i<(ntohs(pa.header.AUTHORITY_COUNT)+ntohs(pa.header.ANSWER_COUNT)+ntohs(pa.header.ADDITONAL_COUNT));i++)
    {
        memcpy(buffer + po,pa.responder[i].name, strlen(pa.responder[i].name) + 1);
        po += strlen(pa.responder[i].name) + 1;
        memcpy(buffer + po, &pa.responder[i].type, sizeof(pa.responder[i].type));
        po += sizeof(pa.responder[i].type);
        memcpy(buffer + po, &pa.responder[i].class, sizeof(pa.responder[i].class));
        po += sizeof(pa.responder[i].class);
        memcpy(buffer + po, &pa.responder[i].ttl, sizeof(pa.responder[i].ttl));
        po += sizeof(pa.responder[i].ttl);
        memcpy(buffer + po, &pa.responder[i].length, sizeof(pa.responder[i].length));
        po += sizeof(pa.responder[i].length);
        memcpy(buffer + po, pa.responder[i].rdata, ntohs(pa.responder[i].length));
        po +=ntohs(pa.responder[i].length);
    }
}//将数据包写入缓存准备发送

void free_packet(mDNS_PACKET *pa) {
    for (int i = 0; i < ntohs(pa->header.QUESTION_COUNT); i++) {
        free(pa->question[i].name);
    }
    for (int i = 0; i < (ntohs(pa->header.AUTHORITY_COUNT) + ntohs(pa->header.ANSWER_COUNT)); i++)
    {
        free(pa->responder[i].name);
        free(pa->responder[i].rdata);
    }
}//释放动态内存

void mDNS_startup(int socket_fd,char *hostname,char *ip){
    char buffer[BUFF_MAX_SIZE];
    bzero(buffer, BUFF_MAX_SIZE);
    int packet_len=0;
    mDNS_PACKET pa;

    set_mDNSheader(&pa.header,0,0x8400,2,0,2,0);
    packet_len+=sizeof(pa.header);

    packet_len+=set_mDNS_QRecord(&pa.question[0],hostname,255,0x0001);

    char temp[20];
    ip4_PTR(temp,ip);
    packet_len+=set_mDNS_QRecord(&pa.question[1],temp,255,0x0001);

    packet_len+=set_mDNS_RRecord(&pa.responder[0],hostname,ip,1,0x0001,120,4,
                                 NOTEXIST,NOTEXIST,NOTEXIST);

    packet_len+=set_mDNS_RRecord(&pa.responder[1],temp,hostname,12,0x0001,120,
                                 strlen(hostname)+2,NOTEXIST,NOTEXIST,NOTEXIST);

    write_data(pa,buffer);

#ifdef Debug
    for(int i=0;i<packet_len;i++)
        printf("%x ",buffer[i]);
    printf("\n");
#endif
    for(int i=0;i<3;i++) {
        usleep(250000);
        mDNS_sendmessage(socket_fd, buffer, packet_len);
    }
    usleep(250000);
#ifdef Debug
    printf("send data to UDP server %s:%d!\n",MDNS_IP,MDNS_PORT);
#endif
    free_packet(&pa);

    packet_len=0;
    bzero(buffer, BUFF_MAX_SIZE);
    set_mDNSheader(&pa.header,0,0x8400,0,2,0,0);
    packet_len+=sizeof(pa.header);

    packet_len+=set_mDNS_RRecord(&pa.responder[0],hostname,ip,1,0x8001,120,4,
                                 NOTEXIST,NOTEXIST,NOTEXIST);

    packet_len+=set_mDNS_RRecord(&pa.responder[1],temp,hostname,12,0x8001,120,
                                 strlen(hostname)+2,NOTEXIST,NOTEXIST,NOTEXIST);

    write_data(pa,buffer);

    for(int i=0;i<7;i++) {
        sleep(1);
        mDNS_sendmessage(socket_fd, buffer, packet_len);
    }
    sleep(1);
#ifdef Debug
    printf("send data to UDP server %s:%d!\n",MDNS_IP,MDNS_PORT);
#endif

}//执行probe步骤

void Probe(int socket_fd,mDNS_resource r)
{
    char buffer[BUFF_MAX_SIZE];
    bzero(buffer, BUFF_MAX_SIZE);
    int packet_len=0;
    mDNS_PACKET pa;

    set_mDNSheader(&pa.header,0,0x8400,1,0,2,0);
    packet_len+=sizeof(pa.header);

    packet_len+=set_mDNS_QRecord(&pa.question[0],r.name,255,0x0001);

    packet_len+=set_mDNS_RRecord(&pa.responder[0],r.name,r.data,r.type,0x8001,120,
                                 strlen(r.data)+8,r.priority,r.weight,r.port);

    packet_len+=set_mDNS_RRecord(&pa.responder[1],r.name,"txtvers=1.ty=Google.id=A",16,0x8001,
                                 4500,strlen("txtvers=1.ty=Google.id=A")+2,NOTEXIST,NOTEXIST,NOTEXIST);

    write_data(pa,buffer);

    usleep(250000);

    for(int i=0;i<2;i++) {
        mDNS_sendmessage(socket_fd, buffer, packet_len);
        usleep(250000);
    }

#ifdef Debug
    printf("send data to UDP server %s:%d!\n",MDNS_IP,MDNS_PORT);
#endif
    free_packet(&pa);
}
void Annouce(int socket_fd,char *hostname,char *ip,mDNS_resource r1)
{
    char buffer[BUFF_MAX_SIZE];
    bzero(buffer, BUFF_MAX_SIZE);
    int packet_len=0;
    mDNS_PACKET pa;

    set_mDNSheader(&pa.header,0,0x8400,0,5,0,0);
    packet_len+=sizeof(pa.header);


    packet_len+=set_mDNS_RRecord(&pa.responder[0],r1.name,r1.data,r1.type,0x8001,120,
                                 strlen(r1.data)+8,r1.priority,r1.weight,r1.port);


    packet_len+=set_mDNS_RRecord(&pa.responder[1],r1.service_domain,r1.name,12,0x0001,4500,
                                 strlen(r1.name)+2,NOTEXIST,NOTEXIST,NOTEXIST);

    packet_len+=set_mDNS_RRecord(&pa.responder[2],"_services._dns-sd._udp.local",
                                 r1.service_domain,12,0x0001,4500,strlen(r1.service_domain)+2,
                                 NOTEXIST,NOTEXIST,NOTEXIST);

    packet_len+=set_mDNS_RRecord(&pa.responder[3],hostname,ip,1,0x8001,120,4,
                                 NOTEXIST,NOTEXIST,NOTEXIST);

    packet_len+=set_mDNS_RRecord(&pa.responder[4],r1.name,"txtvers=1.ty=Google.id=A",16,0x8001,
                                 4500,strlen("txtvers=1.ty=Google.id=A")+2,NOTEXIST,NOTEXIST,NOTEXIST);

    write_data(pa,buffer);

#ifdef Debug
    for(int i=0;i<packet_len;i++)
        printf("%x ",buffer[i]);
    printf("\n");
#endif
    for(int i=0;i<6;i++) {
        mDNS_sendmessage(socket_fd, buffer, packet_len);
        sleep(1);
    }

#ifdef Debug
    printf("send data to UDP server %s:%d!\n",MDNS_IP,MDNS_PORT);
#endif
    free_packet(&pa);
}
