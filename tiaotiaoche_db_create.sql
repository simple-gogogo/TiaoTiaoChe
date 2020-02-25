-- 如果存在名为tiaotiaoche的数据库就删除它
drop database if exists tiaotiaoche;

-- 创建名为tiaotiaoche的数据库并指定默认的字符集和校对规则
create database tiaotiaoche default charset utf8 collate utf8_bin;

-- 切换到tiaotiaoche数据库
use tiaotiaoche;

-- 创建用户表tb_user
create table `tb_user`
(
   `userid`               int auto_increment comment '编号',
   `username`             varchar(20) not null comment '用户名',
   `password`             char(32) not null comment '用户口令',
   `realname`             varchar(20) not null comment '真实姓名',
   `sex`                  bool default 1 comment '性别',
   `tel`                  varchar(20) not null comment '手机号',
   `email`                varchar(255) default '' comment '邮箱',
   `regdate`              datetime default now() comment '注册日期',
   `point`                int default 0 comment '积分',
   `lastvisit`            datetime comment '最后访问时间',
   primary key (`userid`)
);

-- 创建地区表tb_district
create table `tb_district`
(
   `distid`               int not null comment '编号',
   `pid`                  int comment '父级行政单位',
   `name`                 varchar(255) not null comment '名称',
   `ishot`                bool default 0 comment '是否为热门城市',
   `intro`                varchar(255) default '' comment '介绍',
   primary key (`distid`)
);

-- 创建经理人表tb_agent
create table `tb_agent`
(
   `agentid`              int not null auto_increment comment '编号',
   `name`                 varchar(255) not null comment '姓名',
   `tel`                  varchar(20) not null comment '电话',
   `servstar`             int not null default 0 comment '满意度星级',
   `realstar`             int not null default 0 comment '真实度星级',
   `profstar`             int not null default 0 comment '专业度星级',
   `certificated`         bool not null default 0 comment '是否持有专业认证',
   primary key (`agentid`)
);

-- 创建用户登录日志表tb_login_log
create table `tb_login_log`
(
   `logid`                bigint auto_increment comment '编号',
   `userid`               int not null comment '用户',
   `ipaddr`               varchar(255) not null comment 'IP地址',
   `logdate`              datetime default now() comment '登录时间日期',
   `devcode`              varchar(255) default '' comment '设备代码',
   primary key (`logid`)
);

-- 创建店铺表tb_car_shop
create table `tb_car_shop`
(
   `shopid`             int not null auto_increment comment '编号',
   `distid`               int not null comment '所在三级行政区域',
   `name`                 varchar(255) not null comment '名称',
   `hot`                  int default 0 comment '热度',
   `intro`                varchar(511) default '' comment '介绍',
   primary key (`shopid`)
);

-- 创建经理人店铺中间表tb_agent_car_shop
create table `tb_agent_car_shop`
(
   `agent_shopid`      int not null auto_increment comment '编号',
   `agentid`              int not null comment '经理人',
   `shopid`             int not null comment '店铺',
   primary key (`agent_shopid`)
);

-- 创建车型表tb_car_type
create table `tb_car_type`
(
   `typeid`               int comment '编号',
   `name`                 varchar(255) not null comment '名称',
   primary key (`typeid`)
);

-- 创建车信息表tb_car_info
create table `tb_car_info`
(
   `carid`                int not null auto_increment comment '编号',
   `title`                varchar(50) not null comment '车辆名称',
   `price`                int not null comment '价格',
   `priceunit`            varchar(10) not null comment '价格单位',
   `detail`               varchar(511) default '' comment '详情',
   `mainphoto`            varchar(255) not null comment '主图',
   `pubdate`              datetime default now() comment '发布日期',
   `mileage`              varchar(255) not null comment '行驶里程',
   `time`                 datetime comment '首次上牌',
   `gear`                 varchar(255) not null comment '档位/排量',
   `allowremove`          varchar(255) not null comment '准迁移地',
   `hasagentfees`         bool default 0 comment '是否有中介费',
   `typeid`               int not null comment '车型',
   `userid`               int not null comment '发布用户',
   `distid2`              int not null comment '所在二级行政区域',
   `distid3`              int not null comment '所在三级行政区域',
   `car_shopid`           int comment '所在店铺',
   `agentid`              int comment '经理人',
   primary key (`carid`)
);

-- 创建车照片表tb_car_photo
create table `tb_car_photo`
(
   `photoid`              int not null auto_increment comment '编号',
   `carid`              int not null comment '车',
   `path`                 varchar(255) not null comment '资源路径',
   primary key (`photoid`)
);

-- 创建标签表tb_tag
create table `tb_tag`
(
   `tagid`                int auto_increment comment '编号',
   `content`              varchar(20) not null comment '内容',
   primary key (`tagid`)
);

-- 创建车标签中间表tb_car_tag
create table `tb_car_tag`
(
   `car_tag_id`         int auto_increment comment '编号',
   `carid`              int not null comment '车',
   `tagid`                int not null comment '标签',
   primary key (`car_tag_id`)
);

-- 创建用户浏览历史记录表tb_record
create table `tb_record`
(
   `recordid`             bigint auto_increment comment '编号',
   `userid`               int not null comment '用户',
   `carid`              int not null comment '车',
   `recorddate`           datetime not null comment '浏览时间日期',
   primary key (`recordid`)
);

-- 创建角色表tb_role
create table `tb_role`
(
   `roleid`              int auto_increment comment '编号',
   `rolename`            varchar(255) not null comment '角色名',
   primary key (`roleid`)
);

-- 创建权限表tb_privilege
create table `tb_privilege`
(
   `privid`               int auto_increment comment '编号',
   `method`               varchar(15) not null comment '请求方法',
   `url`                  varchar(1024) not null comment '资源的URL',
   `detail`               varchar(255) default '' comment '权限说明',
   PRIMARY KEY (`privid`)
);

-- 创建用户角色中间表tb_user_role
create table `tb_user_role`
(
   `user_role_id`         int auto_increment comment '编号',
   `userid`               int not null comment '用户',
   `roleid`               int not null comment '角色',
   primary key (`user_role_id`)
);

-- 创建角色权限中间表tb_role_privilege
create table `tb_role_privilege`
(
   `role_priv_id`        int auto_increment comment '编号',
   `roleid`               int not null comment '角色',
   `privid`               int not null comment '权限',
   primary key (`role_priv_id`)
);

-- 创建唯一约束
create unique index `uni_idx_agent_car_shop` on `tb_agent_car_shop` (`agentid`, `shopid`);

-- 创建唯一约束
create unique index `uni_idx_record` on `tb_record` (`userid`, `carid`);

-- 创建唯一约束
create unique index `uni_idx_username` on `tb_user` (`username`);

-- 创建唯一约束
create unique index `uni_idx_tel` on `tb_user` (`tel`);

-- 创建唯一约束
create unique index `uni_idx_email` on `tb_user` (`email`);

-- 创建唯一约束
create unique index `uni_idx_car_tag` on `tb_car_tag` (`carid`, `tagid`);

-- 创建外键约束
-- alter table `tb_agent_car_shop` add constraint `fk_agent_car_shop_agentid` foreign key (`agentid`) references `tb_agent` (`agentid`);

-- 创建外键约束
-- alter table `tb_agent_car_shop` add constraint `fk_agent_car_shop_car_shopid` foreign key (`car_shopid`) references `tb_car_shop` (`car_shopid`);

-- 创建外键约束
-- alter table `tb_district` add constraint `fk_district_pid` foreign key (`pid`) references `tb_district` (`distid`);

-- 创建外键约束
-- alter table `tb_car_shop` add constraint `fk_car_shop_distid` foreign key (`distid`) references `tb_district` (`distid`);

-- 创建外键约束
-- alter table `tb_car_info` add constraint `fk_car_info_agentid` foreign key (`agentid`) references tb_agent (`agentid`);

-- 创建外键约束
-- alter table `tb_car_info` add constraint `fk_car_info_distid2` foreign key (`distid2`) references tb_district (`distid`);

-- 创建外键约束
-- alter table `tb_car_info` add constraint `fk_car_info_distid3` foreign key (`distid3`) references tb_district (`distid`);

-- 创建外键约束
-- alter table `tb_car_info` add constraint `fk_car_info_car_shopid` foreign key (`car_shopid`) references tb_car_shop (`car_shopid`);

-- 创建外键约束
-- alter table `tb_car_info` add constraint `fk_car_info_typeid` foreign key (`typeid`) references tb_car_type (`typeid`);

-- 创建外键约束
-- alter table `tb_car_info` add constraint `fk_car_info_userid` foreign key (`userid`) references tb_user (`userid`);

-- 创建外键约束
-- alter table `tb_car_photo` add constraint `fk_car_photo_carid` foreign key (`carid`) references `tb_car_info` (`carid`);

-- 创建外键约束
-- alter table `tb_car_tag` add constraint `fk_car_tag_carid` foreign key (`carid`) references `tb_car_info` (`carid`);

-- 创建外键约束
-- alter table `tb_car_tag` add constraint `fk_car_tag_tagid` foreign key (`tagid`) references `tb_tag` (`tagid`);

-- 创建外键约束
-- alter table `tb_login_log` add constraint `fk_login_log_userid` foreign key (`userid`) references `tb_user` (`userid`);

-- 创建外键约束
-- alter table `tb_record` add constraint `fk_record_carid` foreign key (`carid`) references `tb_car_info` (`carid`);

-- 创建外键约束
-- alter table `tb_record` add constraint `fk_record_userid` foreign key (`userid`) references `tb_user` (`userid`);

-- 创建唯一约束
alter table `tb_user_role` add constraint `uni_user_role` unique (`userid`, `roleid`);

-- 创建唯一约束
alter table `tb_role_privilege` add constraint `uni_role_priv` unique (`roleid`, `privid`);

-- 创建外键约束
-- alter table `tb_role_privilege` add constraint `fk_role_privilege_privid` foreign key (`privid`) references `tb_privilege` (`privid`);

-- 创建外键约束
-- alter table `tb_role_privilege` add constraint `fk_role_privilege_roleid` foreign key (`roleid`) references `tb_role` (`roleid`);

-- 创建外键约束
-- alter table `tb_user_role` add constraint `fk_user_role_roleid` foreign key (`roleid`) references `tb_role` (`roleid`);

-- 创建外键约束
-- alter table `tb_user_role` add constraint `fk_user_role_userid` foreign key (`userid`) references `tb_user` (`userid`);