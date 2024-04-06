import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { SigninComponent } from './signin/signin.component';
import { SignupComponent } from './signup/signup.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { HomepageComponent } from './homepage/homepage.component';

@NgModule({
  declarations: [AppComponent, SigninComponent, SignupComponent, DashboardComponent, HomepageComponent],
  imports: [BrowserModule, 
    FormsModule, 
    HttpClientModule,
    RouterModule.forRoot([
      { path: '', component: HomepageComponent },
      { path: 'signin', component: SigninComponent },
      { path: 'signup', component: SignupComponent },
      { path: 'dashboard', component: DashboardComponent },
    ])
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }