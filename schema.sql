drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text  text not null
);
drop table if exists person;
create table person (
  id integer primary key autoincrement,
  name text not null,
  wageid  varchar(20) not null,
  sex varchar(10)  not null,
  title varchar(20) not null,
  category varchar(20) not null
);
drop table if exists classtech_techer;
create table classtech_techer (
  id integer primary key autoincrement,
  person_id int not null,
  basictech_days int not null,
  shortterm_days int not null,
  totalwork_days int not null,
  systemtraining_machanical_days int not null,--机械综合训练天数
  systemtraining_machanical_stucount int not null,--机械综合训练人数
  systemtraining_other_days int not null,--其它综合训练天数
  compulsorycourse_techhour int not null,--必修课学时
  compulsorycourse_stucount int not null,--必修课人数
  elective_techhour int not null,--选修课学时
  elective_stucount int not null,--选修人数
  graduationproject_stucount int not null,--毕业设计人数
  nuetiac_swjtu int not null,--工程训练大赛校赛National Undergraduate Engineering Training Integration Ability Competition
  nuetiac_sichuan int not null,--工程训练大赛省赛
  nuetiac_nation int not null,--工程训练大赛国赛
  make_techdays int not null,--加工指导天数
  created_time datetime now,
  updated_time datetime now,
  note text not null
);
drop table if exists afterclass_techer;
create table afterclass_techer (
  id integer primary key autoincrement,
  person_id int not null,
  contestproject_swjtu int not null, --实验竞赛活动项目校级
  contestproject_sichuan int not null,--实验竞赛活动省级项目
  contestproject_nation int not null,--国家级实验竞赛活动
  customproject int not null,--个性化实验竞赛项目
  master_course int not null,--研究生课程
  techresearch_swjtu_project int not null,--学校教改项目
  techresearch_etc_newitem int not null,--中心教改项目新开项目
  techresearch_etc_olditem int not null,--中心教改项目现有项目改革
  techresearch_etc_module int not null,--中心教改项目模块改革
  techresearch_etc_course int not null,--中心教改项目课程改革
  techbook int not null,--教材
  paper_c int not null,--C级论文
  paper_issn int not null,--有公开刊号论文
  paper_noissn int not null,--无公开刊号论文
  mapcheck_count int not null,--审核图纸
  course_director int not null,--课程负责人
  project_director int not null,--项目负责人
  master_platfom int not null, --研究生平台
  created_time datetime now,
  updated_time datetime now,
  note text not null

);
drop table if exists classtech_worker;

create table classtech_worker (
  id integer primary key autoincrement,
  person_id int not null,
  basictech_days int not null,
  systemtraining_days int not null,--综合训练天数
  contest_days int not null,--竞赛教学天数
  shortterm_days int not null,--短学期教学天数
  created_time datetime now,
  updated_time datetime now,
  note text not null
);
drop table if exists afterclass_worker;

create table afterclass_worker (
  id integer primary key autoincrement,
  person_id int not null,
  contestproject int not null, --实验竞赛活动项目校级
  techresearch_swjtu_project int not null,--学校教改项目
  techresearch_etc_newitem int not null,--中心教改项目新开项目
  techresearch_etc_olditem int not null,--中心教改项目现有项目改革
  techresearch_etc_module int not null,--中心教改项目模块改革
  techresearch_etc_course int not null,--中心教改项目课程改革
  techbook int not null,--教材
  paper_c int not null,--C级论文
  paper_issn int not null,--有公开刊号论文
  paper_noissn int not null,--无公开刊号论文
  making_nuetiac_days int not null,--工程训练大赛加工
  making_other_days int not null,--其它加工
  created_time datetime now,
  updated_time datetime now,
  note text not null
);
