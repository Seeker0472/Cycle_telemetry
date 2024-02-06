<template>
  <WelcomePage v-if="show == 0" @gotoPage="gotoPage"></WelcomePage>
  <ImportData v-if="show == 1"></ImportData>
  <CreateProject v-if="show == 2"></CreateProject>
  <AllData v-if="show == 3"></AllData>
  <AllProjects v-if="show == 4"></AllProjects>
  <Sync v-if="show == 5"></Sync>
  <About v-if="show == 6"></About>
  <ProjectView v-if="show == 7"></ProjectView>
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
export default {
  components: {
    ProjectView,
    WelcomePage,
    ImportData,
    CreateProject,
    AllData,
    AllProjects,
    Sync,
    About

  },
  // 其他选项...
  data() {
    return {
      "show": 0

    };
  },
  methods: {
    gotoPage(i) {
      this.show = i;
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
