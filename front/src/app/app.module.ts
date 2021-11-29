import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import {RouterModule} from "@angular/router";
import {appRoutes} from "./app.routig";
import { MainpageComponent } from './mainpage/mainpage.component';
import {ProductService} from "./product.service";
import { BrandComponent } from './brand/brand.component';
import { GenerationComponent } from './generation/generation.component';
import {HttpClientModule} from "@angular/common/http";


@NgModule({
  declarations: [
    AppComponent,
    MainpageComponent,
    BrandComponent,
    GenerationComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    HttpClientModule
  ],
  providers: [ProductService],
  bootstrap: [AppComponent],
  exports: [RouterModule],

})
export class AppModule { }
