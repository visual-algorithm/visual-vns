#include<bits/stdc++.h>
#include<vector>
#include <math.h>
#include <random> 
using namespace std;

int CITY_NUMBER = 10;
int SALESMAN_NUMBER = 2;
int DEPOT_NUMBER = 0;

vector<vector<double>> W = {
    {0, 21.4709, 12.0416, 19.2354, 23.4307, 14.2127, 17.4642, 10.6301, 12.8062, 10, 13.4536, },
    {21.4709, 0, 18.1108, 12.2066, 5.09902, 10.0499, 36.7696, 31.9061, 22.8254, 27.5862, 21.0238, },
    {12.0416, 18.1108, 0, 9.43398, 17.2627, 8.06226, 29.1204, 21.0238, 23.0868, 22.0227, 22.8473, },
    {19.2354, 12.2066, 9.43398, 0, 9.21954, 6, 36.6742, 29.4109, 27.0185, 28.4605, 26.0192, },
    {23.4307, 5.09902, 17.2627, 9.21954, 0, 9.84886, 39.8246, 34.0588, 26.9258, 30.8058, 25.2982, },
    {14.2127, 10.0499, 8.06226, 6, 9.84886, 0, 31.3847, 24.7588, 21.0238, 22.8473, 20.025, },
    {17.4642, 36.7696, 29.1204, 36.6742, 39.8246, 31.3847, 0, 9.05539, 16.1555, 9.21954, 18.3848, },
    {10.6301, 31.9061, 21.0238, 29.4109, 34.0588, 24.7588, 9.05539, 0, 16.2788, 8.544, 18.1108, },
    {12.8062, 22.8254, 23.0868, 27.0185, 26.9258, 21.0238, 16.1555, 16.2788, 0, 8, 2.23607, },
    {10, 27.5862, 22.0227, 28.4605, 30.8058, 22.8473, 9.21954, 8.544, 8, 0, 10.0499, },
    {13.4536, 21.0238, 22.8473, 26.0192, 25.2982, 20.025, 18.3848, 18.1108, 2.23607, 10.0499, 0, }
};

vector<vector<int>> T{
    {1,2,3},
    {4,5,6}
};

vector<int> shared_cities = {7,8,9,10};

class City
{
public:
    int city_number;
    int city_color;
    int posx;
    int posy;
    City() {}
    City(int c_n, int c_c, int x, int y)
    {
        city_number = c_n;
        city_color = c_c;
        posx = x;
        posy = y;
    }
};

vector<vector<int>> greedy_initialization(){
    int k = 0;
    int v = 0;
    vector<int> tk(T[k].size()); //T[k](セールスマンkに限定されている都市セット)を一時的に格納
    vector<int> rk(1, 0); //貪欲法で現時点で一番近い都市をここに入れていく
    vector<vector<int>> R(SALESMAN_NUMBER, vector<int>()); //最終的に全てのrkをここに格納
    while (k < SALESMAN_NUMBER){ //各セールスマンのルートについて
        tk = T[k]; //tkに一回移す
        rk.clear();
        v = DEPOT_NUMBER; //拠点から出発しなければならないのでvには最初は拠点をいれる
        rk.push_back(DEPOT_NUMBER);
        for(int i=0;i<T[k].size();i++){ //各限定都市について
            double closest_length = 100000; //vとvに一番近い都市の距離をいれる
            int closest_city_number = DEPOT_NUMBER; //vに一番近い都市の番号をいれる
            for(int j=0;j<tk.size();j++){ //tk内の各都市についてvとの距離を計算
                int pos1 = v; //現在、注目している都市(貪欲法により作成しているルートの先頭)
                int pos2 = tk[j]; //tk内の各都市
                double tkj_length = W[pos1][pos2]; //vとtk[j]の距離をいれる
                if(tkj_length < closest_length){ //vとtk[j]の距離が暫定最小であればclosest_lengthを更新
                    closest_length = tkj_length; 
                    closest_city_number = pos2;
                }
            }
            rk.push_back(closest_city_number); //rkに現在いる都市vに一番近い都市を追加
            v = closest_city_number; //vをルートの先頭に更新
            tk.erase(remove(tk.begin(), tk.end(), closest_city_number), tk.end()); //tkからrkに追加した都市を削除
        }
        rk.push_back(DEPOT_NUMBER); //拠点に帰るのでrkに追加
        R[k] = rk; //最終的なルートのセットRにセールスマンkの貪欲法によるルートを追加
        k++; //注目するセールスマンのルートを変更
    }
    

    vector<int> ex_route(CITY_NUMBER+1); //変更前のルート
    vector<int> new_route(CITY_NUMBER+1); //変更後のルート
    vector<vector<int>> better_routes(SALESMAN_NUMBER, vector<int>()); //各ルートに共有都市を挿入したとき、それぞれ最善のルートセット
    vector<double> ex_route_lengths(SALESMAN_NUMBER, 0); //各ルートにおける共有都市の挿入前の経路長セット
    vector<double> new_route_lengths(SALESMAN_NUMBER, 0); //各ルートにおける共有都市を挿入後の経路長セット
    vector<double> min_route_lengths(SALESMAN_NUMBER, 100000); //各ルートにおける共有都市挿入後の暫定最小の経路長セット
    for(int i=0;i<shared_cities.size();i++){ //各共有都市について
        ex_route = vector<int>(CITY_NUMBER);
        new_route = vector<int>(CITY_NUMBER);
        better_routes = vector<vector<int>>(SALESMAN_NUMBER, vector<int>());
        ex_route_lengths = vector<double>(SALESMAN_NUMBER, 0);
        new_route_lengths = vector<double>(SALESMAN_NUMBER, 0);
        min_route_lengths = vector<double>(SALESMAN_NUMBER, 100000);
        k = 0;
        while(k < SALESMAN_NUMBER){ //各セールスマンのルートについて
            ex_route = R[k]; //限定都市だけを貪欲法で整えたルートを格納
            for(int j=1;j<ex_route.size();j++){ //限定都市だけルートの経路長を計算
                ex_route_lengths[k] += W[ex_route[j-1]][ex_route[j]];
            }
            for(int j=1;j<ex_route.size();j++){ //限定都市だけのルートの都市間のスペースについて(最初と最後は拠点だから含めない)
                new_route = R[k]; //限定都市だけのルートを格納
                new_route_lengths[k] = 0; 
                int a = shared_cities[i]; //都市間のスペースに入れる都市を共有都市セットからいれる
                new_route.insert(new_route.begin()+j, a); //new_routeに共有都市を挿入
                for(int l=1;l<new_route.size();l++){ //共有都市を挿入後の経路長を計算
                    new_route_lengths[k] += W[new_route[l-1]][new_route[l]];
                }

                if(new_route_lengths[k] < min_route_lengths[k]){ //共有都市を挿入後の経路長が暫定最小だったら
                    min_route_lengths[k] = new_route_lengths[k]; //暫定最小経路長を更新
                    better_routes[k] = new_route; //暫定経路を更新
                }
            }
            k++; //注目するセールスマンのルートを変更
        }
        double dif = 0; //挿入後の経路長と挿入前の経路長の差
        double min_dif = 100000; //暫定最小の経路長の差
        int min_salesman_number = 0; //共有都市を挿入するセールスマンの番号(インデックス)
        for(int j=0;j<min_route_lengths.size();j++){ //各ルートについて、経路長の増分が最小になるように共有都市を挿入した場合の経路長セット
            dif = min_route_lengths[j] - ex_route_lengths[j]; //経路長の差の計算
            if(dif < min_dif){ //暫定最小の更新
                min_dif = dif;
                min_salesman_number = j;
            }
        }
        R[min_salesman_number] = better_routes[min_salesman_number]; //共有都市を挿入するとき、増分が最小であるセールスマンのルートを更新
    }

    return R;
}

vector<vector<int>> shaking(vector<vector<int>> x, int s_max){
    vector<vector<vector<int>>> N(0, vector<vector<int>>(SALESMAN_NUMBER, vector<int>())); //s_max個の近傍解(greedy_initializationにおけるR)セット
    vector<vector<int>> new_x(SALESMAN_NUMBER, vector<int>()); //現在の解xの近傍解

    vector<int> cities_numbers;
    for(auto route: x){
        cities_numbers.push_back(route.size());
    }
    int minimum_cities_number = *min_element(cities_numbers.begin(), cities_numbers.end());
    int minimum_cities_index = distance(cities_numbers.begin(), min_element(cities_numbers.begin(), cities_numbers.end()));
    int maximum_cities_index = distance(cities_numbers.begin(), max_element(cities_numbers.begin(), cities_numbers.end()));

    int s = 0; //近傍解のインデックス
    int k, pos1, pos2, relocated_city_number;
    double r; //interchangeかrelocateを決める用の乱数
    //rk = {0,1,2,3,4,5,6,7,0};
    random_device rd; //乱数の種
    mt19937 mt(rd()); //ジェネレータ？
    uniform_real_distribution<double> make_probability(0, 1); //0~1の一様乱数
    uniform_int_distribution<int> make_salesman_number(0, SALESMAN_NUMBER-1); //0~セールスマンの一様乱数
    while(s < s_max){ //s_max個だけ近傍解の作成
        //cout << "while1 start" << endl;
        new_x = x; 
        r = make_probability(mt); //interchangeかrelocateかランダムに決定
        k = make_salesman_number(mt); //どのセールスマンのルートの近傍解を作るかランダムに決定
        vector<int> rk(x[k].size(), 0); //近傍解作成用の変数
        rk = x[k]; //rkにもとの解(ルート)を格納
        if(minimum_cities_number <= 3){
            k = maximum_cities_index;
            rk = x[k];
        }
        if(r < 0.5){ //interchnageをやるとき
            uniform_int_distribution<int> make_change_city_number(1, rk.size()-2); //拠点以外の都市のインデックスを作成
            pos1 = make_change_city_number(mt); //都市のインデックス一つ目
            pos2 = make_change_city_number(mt); //都市のインデックス二つ目
            while(pos1 == pos2){ //pos1とpos2を異なるインデックスにする
                pos2 = make_change_city_number(mt);
            }
            if(pos1 > pos2){ //pos1 > pos2にした方が都合がいい
                int tmp = pos1;
                pos1 = pos2;
                pos2 = tmp;
            }
            int tmp = rk[pos1]; //二つの都市の入れ替え
            rk[pos1] = rk[pos2];
            rk[pos2] = tmp;
            new_x[k] = rk; //近傍解のセールスマンkのルートをinterchangeしたものに更新
        }
        else{ //relocateをやるとき
            uniform_int_distribution<int> make_delete_city_number(1, rk.size()-2);
            pos1 = make_delete_city_number(mt); //都市のインデックス一つ目
            relocated_city_number = rk[pos1]; //場所を変える都市を選択
            rk.erase(remove(rk.begin(), rk.end(), relocated_city_number), rk.end()); //rkから場所を変える都市を削除
            uniform_int_distribution<int> make_insert_city_number(1, rk.size()-2);
            pos2 = make_insert_city_number(mt);
            rk.insert(rk.begin()+pos2, relocated_city_number); //rkの別の場所にさっきの都市を挿入
            new_x[k] = rk; //近傍解のセールスマンkのルートをrelocateしたものに更新
        }
        N.push_back(new_x); //近傍解をNに追加
        s++; //次の近傍解の作成へ
    }

    vector<double> fitnesses(s_max); //近傍解の適応度セット
    vector<double> route_lengths(s_max); //近傍解の経路長セット

    for(int i=0;i<N.size();i++){ //それぞれの近傍解について
        for(int j=0;j<N[i].size();j++){ //それぞれのルートについて
            for(int l=1;l<N[i][j].size();l++){ //それぞれの都市間の距離について
                route_lengths[i] += W[N[i][j][l]][N[i][j][l-1]]; //経路長の計算
            }
        }
    }

    int max_index = distance(route_lengths.begin(), max_element(route_lengths.begin(), route_lengths.end()));
    //経路長セットの中で最大のもののインデックス

    for(int i=0;i<route_lengths.size();i++){ //それぞれの適応度を経路長が最大のものからそれぞれの経路長をひいたものとする
        //fitnesses[i] = route_lengths[max_index] - route_lengths[i];
        fitnesses[i] = 1 / (1 + route_lengths[i]);
    }

    //ルーレット選択の実装方法は少し独特です。
    //まずルーレット選択とは適応度が高いものほど確率の高いルーレットを作り、そこから一つの解を選ぶもの。
    //これを実装するために適応度の累計和配列を作ります。0~1の乱数を作り、適応度の和にかけます。
    //この値が間になるような累計和のインデックスを二分探索で探し、カウント配列のそのインデックスを
    //インクリメントする。こうすることで、適応度が高い解が選ばれる確率の高いルーレットを
    //作成できます。参考にしたサイトではこれを変数trialだけ繰り返していました。そのサイトでは10000回ほど。
    //でもそうすると、カウント配列は確率通りの分布に収束して適応度が一番高い解が必ず選択する
    //ようになってしまいそうですが。

    double total = 0; //ルーレット選択を実行するために必要な適応度の和
    for(int i=0;i<fitnesses.size();i++){
        total += fitnesses[i];
    }

    vector<double> c_sum(fitnesses.size(), 0); //ルーレット選択を実行するために必要な累計和リスト
    c_sum[0] = fitnesses[0];
    for(int i=1;i<fitnesses.size();i++){
        c_sum[i] = c_sum[i-1] + fitnesses[i];
    }

    int trial = 100; //ルーレット選択のパラメータ
    c_sum.insert(c_sum.begin(), 0); //ルーレット選択に必要な操作
    vector<int> count(c_sum.size(), 0); //ルーレット選択に必要なリスト
    for(int i=0;i<trial;i++){
        r = make_probability(mt) * total;
        int low = 0;
        int high = c_sum.size() - 1;
        int mid;
        while(low <= high){
            mid = (low + high) / 2;
            if(c_sum[mid] <= r && r <= c_sum[mid+1]){
                break;
            }
            else if(c_sum[mid+1] < r){
                low = mid + 1;
            }
            else{
                high = mid - 1;
            }
        }
        count[mid+1]++;
    }
    count.erase(count.begin());

    int best_index = distance(count.begin(), max_element(count.begin(), count.end()));

    return N[best_index]; //ルーレット選択で選ばれた解を返す
}


//局所探索用の関数です。
//各都市を一つずつ見ていき、一旦削除するかどうか決めます。一旦削除するものはSという都市セット
//に保管しておきます。全て見終わったあと、S内の都市を経路長の増分が最小になるように挿入します。
//都市セットSが空になったら、最後に2-optによる最適化に入ります。
//各セールスマンのルートの各都市について二都市の付け替えを行い、経路長が短くなるのであれば
//付け替えます。最高のものを返します。
vector<vector<int>> local_search(vector<vector<int>> x){
    vector<vector<int>> exclusive_S(SALESMAN_NUMBER, vector<int>()); //削除する都市のうち限定都市
    vector<int> shared_S; //削除する都市のうち共有都市
    vector<vector<int>> rest_x(SALESMAN_NUMBER, vector<int>()); //削除されなかった残りの都市
    int k = 0;
    double η = 0.1; //都市を削除するかどうかの確率の閾値
    double r;

    random_device rd;
    mt19937 mt(rd());
    uniform_real_distribution<double> make_probability(0, 1); //0~1の一様乱数


    int removed_city_number; //削除した都市の番号のうち現在注目しているもの
    for(int i=0;i<x.size();i++){ //各ルートについて
        rest_x[i] = x[i]; //xは変更したくないのでrest_xに移す
        for(int j=1;j<x[i].size()-1;j++){ //各都市について
            r = make_probability(mt); //削除するかどうかの確率
            if(r < η){ //削除する時
                removed_city_number = x[i][j]; //削除する都市
                rest_x[i].erase(remove(rest_x[i].begin(), rest_x[i].end(), removed_city_number),rest_x[i].end());
                //rest_x[i]から都市を削除
                if(find(shared_cities.begin(), shared_cities.end(), removed_city_number) != shared_cities.end()){
                //もし削除する都市が共有都市だったらshared_Sに格納
                    shared_S.push_back(removed_city_number);
                }
                else{ //そうでないならexclusive_Sに格納
                    exclusive_S[i].push_back(removed_city_number);
                }
            }
        }
    }


    k = 0;
    int a;
    vector<int> new_route;
    vector<double> ex_length(SALESMAN_NUMBER, 0);
    vector<double> min_length(SALESMAN_NUMBER, 100000);
    vector<vector<int>> exclusive_better_routes(SALESMAN_NUMBER, vector<int>());

    exclusive_better_routes = rest_x;

    //基本的にはgreedy_initializationでの操作と同じです。
    //最初に限定都市を残されたルートセットrest_xに増分が最小になるように挿入します。
    for(int i=0;i<exclusive_S.size();i++){ //各ルートについて
        for(int j=0;j<exclusive_S[i].size();j++){ //各ルートの限定都市について
            fill(ex_length.begin(), ex_length.end(), 0); //初期化
            fill(min_length.begin(), min_length.end(), 100000); //初期化
            for(int l=1;l<rest_x[i].size();l++){ //各ルートの残された都市間について
                fill(ex_length.begin(), ex_length.end(), 0);
                new_route = rest_x[i];
                a = exclusive_S[i][j]; 
                new_route.insert(new_route.begin()+l, a);
                for(int o=1;o<new_route.size();o++){ //挿入後の経路長の計算
                    ex_length[i] += W[new_route[o-1]][new_route[o]];
                }
                if(ex_length[i] < min_length[i]){//暫定最小の更新
                    min_length[i] = ex_length[i];
                    exclusive_better_routes[i] = new_route;
                }
            }
            rest_x = exclusive_better_routes; //増分が最小のルートを採用する
        }
    }

    //この時点で、一旦削除されたexclusive_Sは残された都市セットrest_xに挿入されています。
    //ここから共有都市shared_Sをrest_xに挿入していく。
    //このとき、初期化の時と同じように共有都市はどのルートに挿入すべきかまだわからないので
    //共有都市をそれぞれのルートに挿入し、増分が最小になる挿入をした際の経路長を保持し、
    //後から増分が最小なルートを採用する。基本的に初期化の時と同じです。

    
    vector<vector<int>> better_routes(SALESMAN_NUMBER, vector<int>());
    vector<vector<int>> best_routes(SALESMAN_NUMBER, vector<int>());
    vector<double> new_length(SALESMAN_NUMBER, 0);

    best_routes = rest_x;
    for(int i=0;i<shared_S.size();i++){
        fill(ex_length.begin(), ex_length.end(), 0);
        fill(new_length.begin(), new_length.end(), 0);
        fill(min_length.begin(), min_length.end(), 100000);
        k = 0;
        while(k < SALESMAN_NUMBER){
            better_routes[k] = best_routes[k];
            for(int j=1;j<better_routes[k].size();j++){
                ex_length[k] += W[better_routes[k][j-1]][better_routes[k][j]];
            }
            for(int j=1;j<better_routes[k].size()-1;j++){
                new_route = best_routes[k];
                new_length[k] = 0;
                a = shared_S[i];
                new_route.insert(new_route.begin()+j, a);

                for(int l=1;l<new_route.size();l++){
                    new_length[k] += W[new_route[l-1]][new_route[l]];
                }
                if(new_length[k] < min_length[k]){
                    min_length[k] = new_length[k];
                    better_routes[k] = new_route;
                }
            }
            k++;
        }
        double dif = 0;
        double min_dif = 100000;
        int min_salesman_number = 0;
        for(int j=0;j<min_length.size();j++){
            dif = min_length[j] - ex_length[j];
            if(dif < min_dif){
                min_dif = dif;
                min_salesman_number = j;
            }

            
        }
        best_routes[min_salesman_number] = better_routes[min_salesman_number];
    }


    //2-optを実装します。
    //二つの都市を付け替えます。具体的な操作としては二つの都市を入れ替えた後、
    //ルート上に置いて、二つの都市の間の都市の順番を逆にします。
    int index, pos1, pos2; 
    double two_opted_length, min_two_opted_length;
    vector<int> reversed_cities; //二つの都市間の順番を逆にした都市を格納する
    vector<int> better_route; //2-optを試行し、経路長が改善された場合、一旦ここに格納する
    vector<int>two_opted_route(SALESMAN_NUMBER);
    for(int i=0;i<best_routes.size();i++){//各ルートについて
        min_two_opted_length = 100000; //大きめの値で初期化
        better_route = best_routes[i];
        for(int j=1;j<best_routes[i].size()-2;j++){ //各pos1について
        two_opted_route = best_routes[i];
            for(int l=j;l<best_routes[i].size()-1;l++){ //各pos2について
                for(int o=j;o<=l;o++){//pos1とpos2間の各都市について
                    reversed_cities.push_back(best_routes[i][o]); //逆にする都市を一旦順序通り格納
                }
                reverse(reversed_cities.begin(), reversed_cities.end()); //逆順にする
                index = 0; //逆順にした都市の配列を操作する用のインデックス
                for(int o=j;o<=l;o++){ //二つの都市間の都市を逆順に
                    two_opted_route[o] = reversed_cities[index]; 
                    index++;
                }

                two_opted_length = 0; //2-optで改善したルートの経路長の計算
                for(int o=1;o<two_opted_route.size();o++){
                    two_opted_length += W[two_opted_route[o-1]][two_opted_route[o]];
                }
                if(two_opted_length < min_two_opted_length){ //暫定最小の更新
                    min_two_opted_length = two_opted_length;
                    better_route = two_opted_route;
                }
            }
        }
        best_routes[i] = better_route; //経路長最小のルートでbest_routesの更新
    }

    return best_routes; //最良のルートを返す
}

void evaluation(void){
    vector<vector<int>> initial_solution;
    vector<vector<int>> shaked_solution;
    vector<vector<int>> better_solution;

    initial_solution = greedy_initialization();

    int cnt = 0;
    int all_cnt = 0;
    double min_value = 100000;

    vector<double> initial_solution_lengths(SALESMAN_NUMBER, 0);
    for(int i=0;i<initial_solution.size();i++){
        for(int j=1;j<initial_solution[i].size();j++){
            initial_solution_lengths[i] += W[initial_solution[i][j-1]][initial_solution[i][j]];
        }
    }

    double initial_value = initial_solution_lengths[0] + initial_solution_lengths[1];
    cout << "initial value: " << initial_value << endl;

    vector<vector<int>> optimal_solution(SALESMAN_NUMBER, vector<int>());
    optimal_solution = initial_solution;
    min_value = initial_value;
    while(cnt < 10000){
        shaked_solution = shaking(initial_solution, 10);
        better_solution = local_search(shaked_solution);

        vector<double> solution_lengths(SALESMAN_NUMBER, 0);
        for(int i=0;i<better_solution.size();i++){
            for(int j=1;j<better_solution[i].size();j++){
                solution_lengths[i] += W[better_solution[i][j-1]][better_solution[i][j]];
            }
        }
        
        double value = solution_lengths[0] + solution_lengths[1];
        if(value < min_value){
            min_value = value;
            optimal_solution = better_solution;
            cnt = 0;
            cout << "min_value: " << min_value << endl;
        }
        cnt++;
        all_cnt++;
    }

    cout << "optimal value is " << min_value << endl;
    cout << "optimal solution is " << endl;
    for(auto route: optimal_solution){
        for(auto city: route){
            cout << city << ", ";
        }
        cout << endl;
    }
    cout << "all_cnt is " << all_cnt << endl;
    cout << endl;
}

int main(void){
    int N = 10;
    int M = 2;
    vector<int> U = {1,2,3,4,5,6,7,8,9,10};
    int lv1, lv2;
    vector<string> indexes = {"i", "j", "k", "l", "m", "o", "p", "q", "r", "s"};
    vector<City> cities;

    cities.push_back(City(0, 0, 42, 41));
    cities.push_back(City(1, 0, 32, 22));
    cities.push_back(City(2, 0, 30, 40));
    cities.push_back(City(3, 0, 25, 32));
    cities.push_back(City(4, 0, 27, 23));
    cities.push_back(City(5, 0, 31, 32));
    cities.push_back(City(6, 0, 58, 48));
    cities.push_back(City(7, 0, 49, 49));
    cities.push_back(City(8, 0, 52, 33));
    cities.push_back(City(9, 0, 52, 41));
    cities.push_back(City(10, 0, 51, 31));

    evaluation();

    return 0;
}




