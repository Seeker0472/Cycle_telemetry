<template>
  <WelcomePage v-if="show == 0 || show == 2 || show == 8 || show == 1 || show == 2 || show == 2" @gotoPage="gotoPage">
  </WelcomePage>
  <ImportData ref="importData"></ImportData>
  <CreateProject ref="CreateProject"></CreateProject>
  <AllData v-if="show == 3" @gotoPage="gotoPage"></AllData>
  <AllProjects v-if="show == 4" @gotoPage="gotoPage"></AllProjects>
  <Sync v-if="show == 5"></Sync>
  <About v-if="show == 6"></About>
  <ProjectView v-if="show == 7" :cutid="cutid"></ProjectView>
  <addAccount ref="addAccount"></addAccount>
</template>


<script>

import ProjectView from './components/ProjectView.vue';
import WelcomePage from './components/WelcomePage.vue';
import ImportData from './components/importData.vue';
import CreateProject from './components/CreateProject.vue';
import AllData from './components/allData.vue';
import AllProjects from './components/allProjects.vue';
import Sync from './components/SyncView.vue';
import About from './components/AboutPage.vue';
import addAccount from './components/addAccount.vue';
import { ref } from 'vue'
export default {
  setup() {
    const show = ref(0)
    const cutid = ref("X")
    return {
      show,
      cutid
    }
  },
  components: {
    ProjectView,
    WelcomePage,
    ImportData,
    CreateProject,
    AllData,
    AllProjects,
    Sync,
    About,
    addAccount,

  },
  // 其他选项...
  // data() {
  //   return {
  //     "show": 0,
  //     "cutid": "0",

  //   };
  // },
  methods: {
    gotoPage(i, j) {
      this.show = i;
      if (j) {
        this.cutid = j;
        console.log(this.cutid)
      }
      if (i == 2) {
        this.$refs.CreateProject.showWindow();
      }
      if (i == 8) {
        this.$refs.addAccount.showWindow();
      }
      if (i == 1) {
        this.$refs.importData.showWindow();
      }
    }
  },
  mounted() {

  }
};
</script>

<style>
/* body {
  margin: 0px;
} */
</style>
