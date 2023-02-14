<template>
    <nav>
        <v-app-bar class="px-10">
            <a href="/">
                <img height="45" src="/img/e-rihs-logo.svg" alt="Access-DS" />
            </a>
            <v-spacer></v-spacer>
    
            <v-btn
                text
                to="/generic"
                class="hidden-sm-and-down"
                color="grey darken-2"
            >
                <v-icon left>mdi-folder-open</v-icon>
                Generic record entry
            </v-btn>
    
            <v-btn
                text
                to="/project"
                class="hidden-sm-and-down"
                color="grey darken-2"
            >
                <v-icon left>mdi-folder-open</v-icon>
                Project workflow
            </v-btn>
    
            <v-divider vertical class="hidden-sm-and-down"></v-divider>
    
            <v-btn text class="hidden-sm-and-down" color="grey darken-2" disabled>
                <v-icon left>mdi-cog</v-icon>
            </v-btn>
    
            <v-app-bar-nav-icon
                class="hidden-md-and-up"
                @click="appBarDropdown = true"
            ></v-app-bar-nav-icon>
        </v-app-bar>
    
        <v-navigation-drawer v-model="appBarDropdown" absolute temporary right>
            <v-list nav dense>
                <v-list-item-group color="primary">
                    <v-list-item to="/generic">
                        <v-list-item-icon>
                            <v-icon>mdi-folder-open</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Generic record entry</v-list-item-title>
                    </v-list-item>
    
                    <v-list-item to="/project">
                        <v-list-item-icon>
                            <v-icon>mdi-folder-open</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Project workflow</v-list-item-title>
                    </v-list-item>
    
                    <v-divider></v-divider>
                    <v-list-item>
                        <v-list-item-icon>
                            <v-icon>mdi-cog</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Settings</v-list-item-title>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>
    </nav>
</template>

<script>
export default {
    data() {
        return {
            appBarDropdown: false,
        }
    },
}</script>

<style scoped></style>
