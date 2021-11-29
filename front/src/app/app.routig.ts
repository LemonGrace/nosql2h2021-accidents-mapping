import {Routes} from "@angular/router";
import {MainpageComponent} from "./mainpage/mainpage.component";
import {BrandComponent} from "./brand/brand.component";
import {GenerationComponent} from "./generation/generation.component";


export const appRoutes: Routes = [
  {
    path: "",
    component: MainpageComponent,
  },
  {
    path: ':brand/:model',
    component: GenerationComponent
  },
  {
    path: ':brand',
    component: BrandComponent,
  }
]
