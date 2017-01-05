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
drop table if exists classtech_teacher;
create table classtech_teacher (
  id integer primary key autoincrement,
  person_id int not null,
  basictech_days NUMERIC not null,--基础教学天数
  shortterm_days NUMERIC not null,--短学期教学天数
  totalwork_days NUMERIC not null,--总工作天数
  systemtraining_machanical_days NUMERIC not null,--机械综合训练天数
  systemtraining_machanical_stucount NUMERIC not null,--机械综合训练人数
  systemtraining_other_days NUMERIC not null,--其它综合训练天数
  compulsorycourse_techhour NUMERIC not null,--必修课学时
  compulsorycourse_stucount NUMERIC not null,--必修课人数
  elective_techhour NUMERIC not null,--选修课学时
  elective_stucount NUMERIC not null,--选修人数
  graduationproject_stucount NUMERIC not null,--毕业设计人数
  nuetiac_swjtu NUMERIC not null,--工程训练大赛校赛National Undergraduate Engineering Training NUMERICegration Ability Competition
  nuetiac_sichuan NUMERIC not null,--工程训练大赛省赛
  nuetiac_nation NUMERIC not null,--工程训练大赛国赛
  make_techdays NUMERIC not null,--加工指导天数
  created_time datetime now,
  updated_time datetime now,
  note text not null  --备注
);
drop table if exists afterclass_teacher;
create table afterclass_teacher (
  id integer primary key autoincrement,
  person_id int not null,
  contestproject_swjtu NUMERIC not null, --实验竞赛活动项目校级
  contestproject_sichuan NUMERIC not null,--实验竞赛活动省级项目
  contestproject_nation NUMERIC not null,--国家级实验竞赛活动
  customproject NUMERIC not null,--个性化实验竞赛项目
  master_course NUMERIC not null,--研究生课程
  techresearch_swjtu_project NUMERIC not null,--学校教改项目
  techresearch_etc_newitem NUMERIC not null,--中心教改项目新开项目
  techresearch_etc_olditem NUMERIC not null,--中心教改项目现有项目改革
  techresearch_etc_module NUMERIC not null,--中心教改项目模块改革
  techresearch_etc_course NUMERIC not null,--中心教改项目课程改革
  techbook NUMERIC not null,--教材
  paper_c NUMERIC not null,--C级论文
  paper_issn NUMERIC not null,--有公开刊号论文
  paper_noissn NUMERIC not null,--无公开刊号论文
  mapcheck_count NUMERIC not null,--审核图纸
  course_director NUMERIC not null,--课程负责人
  project_director NUMERIC not null,--项目负责人
  master_platfom NUMERIC not null, --研究生平台
  created_time datetime now,
  updated_time datetime now,
  note text not null

);
drop table if exists classtech_worker;

create table classtech_worker (
  id integer primary key autoincrement,
  person_id int not null,
  basictech_days NUMERIC not null,--基础教学天数
  systemtraining_days NUMERIC not null,--综合训练天数
  contest_days NUMERIC not null,--竞赛教学天数
  shortterm_days NUMERIC not null,--短学期教学天数
  created_time datetime now,
  updated_time datetime now,
  note text not null
);
drop table if exists afterclass_worker;

create table afterclass_worker (
  id integer primary key autoincrement,
  person_id int not null,
  contestproject NUMERIC not null, --实验竞赛活动项目校级
  techresearch_swjtu_project NUMERIC not null,--学校教改项目
  techresearch_etc_newitem NUMERIC not null,--中心教改项目新开项目
  techresearch_etc_olditem NUMERIC not null,--中心教改项目现有项目改革
  techresearch_etc_module NUMERIC not null,--中心教改项目模块改革
  techresearch_etc_course NUMERIC not null,--中心教改项目课程改革
  techbook NUMERIC not null,--教材
  paper_c NUMERIC not null,--C级论文
  paper_issn NUMERIC not null,--有公开刊号论文
  paper_noissn NUMERIC not null,--无公开刊号论文
  making_nuetiac_days NUMERIC not null,--工程训练大赛加工
  making_other_days NUMERIC not null,--其它加工
  created_time datetime now,
  updated_time datetime now,
  note text not null
);

drop table if exists inno_days;

create table inno_days (
  id integer primary key autoincrement,
  person_id int not null,
  inno_days NUMERIC not null,--折合后创新实践工作日数
  created_time datetime now,
  updated_time datetime now,
  note text not null
);


drop table if exists factors_teacher;

create table factors_teacher (
  id integer primary key autoincrement,
  person_id int not null,
  s_evaluation NUMERIC not null,--S权重
  s_environment NUMERIC not null,--S环境系数
  s_temperature NUMERIC not null,--S高温系数

  created_time datetime now,
  updated_time datetime now,
  note text not null
);

drop table if exists factors_worker;

create table factors_worker (
  id integer primary key autoincrement,
  person_id int not null,
  s_evaluation NUMERIC not null,--S权重
  s_environment NUMERIC not null,--S环境系数
  s_temperature NUMERIC not null,--S高温系数

  created_time datetime now,
  updated_time datetime now,
  note text not null
);
