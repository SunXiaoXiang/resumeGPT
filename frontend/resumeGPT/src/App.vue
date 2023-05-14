<template>
  <div class="container">
    <div class="left">
      姓名: <br><span>{{ resume.name }}</span><br>  
      年龄: <br><span>{{ resume.age }}</span><br>   
      技能: <br><span>{{ resume.skills }}</span><br>
      经历: <br><span>{{ resume.experiences }}</span><br>
    </div>
    <div class="right">
      chatgpt：<button @click="summaryExpes">工作经历缩写100字</button>
      字数：<br><span>{{ summaryLen }}</span><br>
      经历概述：<br><span>{{ summaryText }}</span><br>
      chatgpt：<button @click="correct_Text">文本纠错</button>
      纠错后文字：<br><span>{{ correctLen }}</span><br>
      纠错后文字：<p v-html="correctText.trim()"></p><br>
      chatgpt：<button @click="completeDetails">简历中的公司和技术</button>
      公司：<br><span>{{ company }}</span><br>
      公司简介：<br><span>{{ companyDetail }}</span><br>
      IT技术：<br><span>{{ Technology }}</span><br>
      IT技术简介：<br><span>{{ TechnologyDetail }}</span><br>
      chatgpt：<button @click="showDetails">公司及技术情况</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      resume: {},
      summaryText: "",
      summaryLen: "",
      correctLen:"",
      correctText:"",
      company:"",
      companyDetail:"",
      Technology:"",
      TechnologyDetail:""
    };
  },
  mounted() {
    axios.get('http://localhost:8000/resumes')
      .then((response) => {
        this.resume = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
  methods: {
    summaryExpes() {
      axios.get('http://localhost:8000/summary')
        .then((response) => {
          this.summaryLen = response.data.summaryLen;
          this.summaryText = response.data.summaryText
        })
        .catch((error) => {
          console.log(error);
        });
    },
    correct_Text() {
      axios.get('http://localhost:8000/correct')
        .then((response) => {
          this.correctLen = response.data.correctLen;
          this.correctText = response.data.correctText
        })
        .catch((error) => {
          console.log(error);
        });
    },
    completeDetails() {
      axios.get('http://localhost:8000/entities')
        .then((response) => {
          this.company = response.data.company;
          this.Technology = response.data.Technology
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showDetails() {
      axios.get('http://localhost:8000/searchEntities', {
        params: {
          company: this.company,
          skills: this.Technology
        }
      })
        .then((response) => {
          this.companyDetail = response.data.companyD;
          this.TechnologyDetail = response.data.techD
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>