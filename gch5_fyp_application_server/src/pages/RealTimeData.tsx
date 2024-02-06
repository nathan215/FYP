import TTNDataFetcher from "../components/TTN_StorageIntegration";
import Wrapper from "../components/Wrapper";

const RealTimeData = () => {
  return (
    // <div>
    //   <Orders />
    // </div>
    <>
      <Wrapper title="Data Storage">
        <TTNDataFetcher></TTNDataFetcher>
      </Wrapper>
    </>
  );
};

export default RealTimeData;
