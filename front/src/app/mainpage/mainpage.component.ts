import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {IItemsResponse, ProductService} from "../product.service";
import {Navigation, Router} from "@angular/router";

@Component({
  selector: 'app-mainpage',
  templateUrl: './mainpage.component.html',
  styleUrls: ['./mainpage.component.css']
})
export class MainpageComponent implements OnInit {
  @ViewChild('input') public $InputElement: ElementRef | undefined;
  public Brands: IItemsResponse[] | undefined;
  public Init: boolean = false;
  public Result: IItemsResponse[] | undefined;

  constructor(
    protected productService: ProductService,
    protected nav: Router
  ) {
  }

  public async ngOnInit(): Promise<void> {
    this.Brands = await this.productService.GetBrands()
    this.Init = true;
  }

  public async GoNext(brandName: string): Promise<void> {
    await this.nav.navigate([`/${brandName}`]);
  }

  public FindBrand(e: Event): void {
    const value = this.$InputElement?.nativeElement.value;
    console.log(value)
    if (!value){
      this.Result = [];
      return;
    }
    if (!this.Brands)
      return;
    this.Result = this.Brands.filter(_brand => _brand.brand.includes(value));
  }

}
